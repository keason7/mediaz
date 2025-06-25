"""Compression functions."""

import shutil
import time

import pandas as pd
from tqdm import tqdm

from mediaz.dtype.dtype import get_media_obj
from mediaz.dtype.dtype_support import DataTypesOut
from mediaz.utils import get_files_paths, get_logger

logger = get_logger(__name__)


def compress(path_in, path_out, compress_params, stats):
    """Compress a supported media file.

    Args:
        path_in (pathlib.Path): Input file path.
        path_out (pathlib.Path): Output file path.
        compress_params (dict): Compression parameters.
        stats (pandas.Dataframe): Statistics dataframe.

    Returns:
        pandas.Dataframe: Updated statistics dataframe.
    """
    current_stats = {
        "in_path": [str(path_in)],
        "in_size": [],
        "out_path": [str(path_out)],
        "out_size": [],
        "compression_ratio": [],
        "status": [],
    }

    # get the right media object based on input dtype
    media = get_media_obj(path_in, path_out)

    # unknown input dtype, we copy the input file to output directory
    if media is None:
        logger.info("Copy file because of unknown input format: %s", path_in)
        path_out = path_out.parent / f"{path_in.stem}{path_in.suffix.lower()}"
        shutil.copy2(path_in, path_out)
        current_stats["status"].append(0)

    # read, compress and write
    else:
        media.read(str(path_in))
        media.write(str(path_out), compress_params)
        current_stats["status"].append(1)

    current_stats["in_size"].append(path_in.stat().st_size)
    current_stats["out_size"].append(path_out.stat().st_size)
    current_stats["compression_ratio"].append(current_stats["in_size"][0] / current_stats["out_size"][0])

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
            "out_size": [],
            "compression_ratio": [],
            "status": [],
        }
    )

    logger.info("Starting compression on %s files.", len(path_in_files))
    start = time.time()

    # compression task
    for idx, path_in_file in enumerate(tqdm(path_in_files, disable=no_progress_bar)):
        stats = compress(path_in_file, path_out_files[idx], config["compress_params"], stats)

    logger.info("Task took %s minutes.", (time.time() - start) / 60)

    logger.info("Writing statistics file.")
    path_stats = path_summary / "stats.json"
    stats.to_json(str(path_stats))
