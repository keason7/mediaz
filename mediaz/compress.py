"""Compression functions."""

import shutil
import time

import pandas as pd
from tqdm import tqdm

from mediaz.dtype.dtype import get_media_obj
from mediaz.dtype.dtype_support import DataTypesOut
from mediaz.utils import get_files_paths, get_logger, update_stats, verify_number_of_files

logger = get_logger(__name__)


def copy_input(path_in, path_out, current_stats):
    """Copy unrecognized input file.

    Args:
        path_in (pathlib.Path): Input file path.
        path_out (pathlib.Path): Output file path.
        current_stats (pandas.Dataframe): Statistics dataframe.

    Returns:
        pandas.Dataframe: Statistics dataframe.
    """
    logger.info("Copy file because of unknown input format: %s", path_in)

    # copy input file as output file
    path_out = path_out.parent / f"{path_in.stem}{path_in.suffix.lower()}"
    shutil.copy2(path_in, path_out)

    # add output path, sizes and status
    current_stats = update_stats(
        current_stats,
        {
            "out_path": str(path_out),
            "out_compressed_size": path_out.stat().st_size,
            "out_size": path_out.stat().st_size,
            "status": 0,
        },
    )
    return current_stats


def compress_input(path_in, path_out, media, config, current_stats):
    """Compressed recognized input media file.

    Args:
        path_in (pathlib.Path): Input file path.
        path_out (pathlib.Path): Output file path.
        media (ImageMedia or VideoMedia): Media object.
        config (dict): Config dictionary.
        current_stats (pandas.Dataframe): Statistics dataframe.

    Returns:
        pandas.Dataframe: Statistics dataframe.
    """
    try:
        media.read(str(path_in))
        media.write(str(path_out), config["compress_params"])

        # add output path, compressed size and status
        current_stats = update_stats(
            current_stats,
            {
                "out_path": str(path_out),
                "out_compressed_size": path_out.stat().st_size,
                "status": 1,
            },
        )

        # compression has failed (larger outpur file size)
        if path_in.stat().st_size < path_out.stat().st_size:
            # replace compressed file by the original file
            if config["copy_if_larger"]:
                logger.info(
                    "Compressed file larger than original, compressed file is replaced by original: %s",
                    str(path_in),
                )

                # remove compressed file
                path_out.unlink(missing_ok=False)

                # copy input file as output file
                path_out = path_out.parent / f"{path_in.stem}{path_in.suffix.lower()}"
                shutil.copy2(path_in, path_out)

                # update output path and status since it has changed
                current_stats = update_stats(current_stats, {"out_path": str(path_out), "status": 2})

            # keep compressed file as output file
            else:
                logger.info("Compressed file larger than original: %s", str(path_in))

        # add final output file size in stats
        current_stats = update_stats(current_stats, {"out_size": path_out.stat().st_size})

    except Exception:
        logger.error("Failed to compress file: %s, file will be copied.", path_in)

        path_out = path_out.parent / f"{path_in.stem}{path_in.suffix.lower()}"
        shutil.copy2(path_in, path_out)

        current_stats = update_stats(
            current_stats,
            {
                "out_path": str(path_out),
                "out_compressed_size": path_out.stat().st_size,
                "out_size": path_out.stat().st_size,
                "status": 3,
            },
        )

    return current_stats


def compress(path_in, path_out, config, stats):
    """Compress a supported media file.

    Args:
        path_in (pathlib.Path): Input file path.
        path_out (pathlib.Path): Output file path.
        config (dict): Config dictionary.
        stats (pandas.Dataframe): Statistics dataframe.

    Returns:
        pandas.Dataframe: Updated statistics dataframe.
    """
    current_stats = {
        "in_path": [],
        "in_size": [],
        "out_path": [],
        "out_compressed_size": [],
        "out_size": [],
        "status": [],
    }

    # add input path and size values to statistics
    current_stats = update_stats(current_stats, {"in_path": str(path_in), "in_size": path_in.stat().st_size})

    # get the right media object based on input dtype
    media = get_media_obj(path_in, path_out)

    # unknown input dtype, we copy the input file to output directory
    if media is None:
        current_stats = copy_input(path_in, path_out, current_stats)

    # read, compress and write
    else:
        current_stats = compress_input(path_in, path_out, media, config, current_stats)

    return pd.concat((stats, pd.DataFrame(data=current_stats)), ignore_index=True)


def bulk_compress(config, path_in, path_data, path_summary, no_progress_bar):
    """Compress all supported medias within an input directory.

    Args:
        config (dict): Config dictionary.
        path_in (pathlib.Path): Input directory path.
        path_data (pathlib.Path): Project data path.
        path_summary (pathlib.Path): Project summary path.
        no_progress_bar (bool): Enable or disable tqdm progress bar.

    Raises:
        KeyError: Invalid out dtype keys.
        TypeError: Invalid output format.
    """
    # check type of medias keys in output format dict
    expected_keys = ["image", "video"]
    if sorted(list(config["out_dtype"].keys())) != sorted(expected_keys):
        raise KeyError(f"Invalid out dtype keys. Expect {expected_keys}, but found {list(config['out_dtype'].keys())}")

    # check that each ouput format is allowed
    for _, dtype in config["out_dtype"].items():
        if dtype["fmt"] not in DataTypesOut.keys():
            raise TypeError(f"Invalid output format. Available output formats: {list(DataTypesOut.keys())}")

    # get all input files and output files paths
    path_in_files, path_out_files = get_files_paths(path_in, path_data, config["out_dtype"])

    stats = pd.DataFrame(
        data={
            "in_path": [],
            "in_size": [],
            "out_path": [],
            "out_compressed_size": [],
            "out_size": [],
            "status": [],
        }
    )

    logger.info("Starting compression on %s files.", len(path_in_files))
    start = time.time()

    # compression task
    for idx, path_in_file in enumerate(tqdm(path_in_files, disable=no_progress_bar)):
        logger.info("Compressing file: %s", str(path_in_file))
        stats = compress(path_in_file, path_out_files[idx], config, stats)

    logger.info("Task took %s minutes.", (time.time() - start) / 60)

    logger.info("Writing statistics file.")
    path_stats = path_summary / "stats.json"
    stats.to_json(str(path_stats))

    verify_number_of_files(path_in, path_data)
