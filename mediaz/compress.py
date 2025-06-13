"""Compression functions."""

import shutil

from tqdm import tqdm

from mediaz.dtype.dtype import get_media_obj
from mediaz.dtype.dtype_support import DataTypesOut
from mediaz.utils import get_files_paths


def compress(path_in, path_out, compress_params):
    """Compress a supported media file.

    Args:
        path_in (pathlib.Path): Input file path.
        path_out (pathlib.Path): Output file path.
        compress_params (dict): Compression parameters.
    """
    # get the right media object based on input dtype
    media = get_media_obj(path_in, path_out)

    # unknown input dtype, we copy the input file to output directory
    if media is None:
        path_out = path_out.parent / f"{path_in.stem}{path_in.suffix.lower()}"
        shutil.copy2(path_in, path_out)

    # read, compress and write
    else:
        media.read(str(path_in))
        media.write(str(path_out), compress_params)


def bulk_compress(config, path_in, path_project):
    """Compress all supported medias within an input directory.

    Args:
        config (dict): Config dictionary.
        path_in (pathlib.Path): Input directory path.
        path_project (pathlib.Path): Project path.

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
    path_in_files, path_out_files = get_files_paths(path_in, path_project, config["out_dtype"])

    # compression task
    for idx, path_in_file in enumerate(tqdm(path_in_files)):
        compress(path_in_file, path_out_files[idx], config["compress_params"])
