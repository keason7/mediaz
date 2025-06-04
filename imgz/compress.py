from pathlib import Path

from imgz.image.standard_image import StandardImage
from imgz.utils import create_project, sanitize_paths

_out_formats = {"JPEG": ".jpg"}


def compress(path_in, path_out, out_data_type):
    standard_image = StandardImage()

    standard_image.read(path_in)
    standard_image.write(path_out, out_data_type)


def bulk_compress(path_in, out_data_type="JPEG"):

    path_in = Path(path_in).expanduser()
    path_project = create_project(path_in)

    path_in_files = [path for path in path_in.rglob("*") if path.is_file()]
    path_out_files = [
        path_project / path_in_file.relative_to(path_in).with_suffix(_out_formats[out_data_type])
        for path_in_file in path_in_files
    ]

    path_out_files = sanitize_paths(path_out_files)

    for idx, path_in_file in enumerate(path_in_files):
        compress(path_in_file, path_out_files[idx], out_data_type)
