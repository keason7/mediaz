"""Compress functions."""

import shutil
from pathlib import Path

from tqdm import tqdm

from mediaz.dtype.dtype import get_media_type
from mediaz.dtype.dtype_support import DataTypesOut
from mediaz.utils import get_files_paths


def compress(path_in, path_out, compression):
    media = get_media_type(path_in, path_out)

    if media is None:
        path_out = Path(path_out).parent / f"{path_in.stem}{path_in.suffix.lower()}"
        shutil.copy2(path_in, path_out)

    else:
        media.read(str(path_in))
        media.write(str(path_out), compression)


def bulk_compress(path_in, path_project, config):
    expected_keys = ["image", "video"]

    if sorted(list(config["out_dtype"].keys())) != sorted(expected_keys):
        raise KeyError(f"Invalid out dtype keys. Expect {expected_keys}, but found {list(config['out_dtype'].keys())}")

    for _, dtype in config["out_dtype"].items():
        if dtype["fmt"] not in DataTypesOut.keys():
            raise TypeError(f"Invalid output format. Available output formats: {list(DataTypesOut.keys())}")

    path_in_files, path_out_files = get_files_paths(path_in, path_project, config["out_dtype"])

    for idx, path_in_file in enumerate(tqdm(path_in_files)):
        compress(path_in_file, path_out_files[idx], config["compression"])
