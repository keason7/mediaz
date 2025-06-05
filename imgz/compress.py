from pathlib import Path

from imgz.image.standard_image import StandardImage
from imgz.utils import create_project, get_files_paths


def compress(path_in, path_out, out_data_type):
    standard_image = StandardImage()

    standard_image.read(path_in)
    standard_image.write(path_out, out_data_type)


def bulk_compress(path_in, path_project, out_data_type="JPEG"):

    path_in_files, path_out_files = get_files_paths(path_in, path_project, out_data_type)

    for idx, path_in_file in enumerate(path_in_files):
        compress(path_in_file, path_out_files[idx], out_data_type)
