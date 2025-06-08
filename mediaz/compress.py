import shutil
from pathlib import Path

from mediaz.dtype.dtype import get_media_type
from mediaz.utils import get_files_paths


def compress(path_in, path_out):
    media, dtype = get_media_type(path_in)

    if dtype is None:
        path_out = Path(path_out).parent / f"{path_in.stem}{path_in.suffix.lower()}"
        shutil.copy2(path_in, path_out)

    else:
        media.read(str(path_in), dtype["fmt"])
        media.write(path_out)


def bulk_compress(path_in, path_project, out_dtype):
    path_in_files, path_out_files = get_files_paths(path_in, path_project, out_dtype)

    for idx, path_in_file in enumerate(path_in_files):
        compress(path_in_file, path_out_files[idx])
