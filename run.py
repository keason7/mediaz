import argparse
from pathlib import Path

from imgz.compress import bulk_compress
from imgz.utils import create_project


def main(path_directory):
    path_directory = Path(path_directory).expanduser()
    path_project = create_project(path_directory)

    bulk_compress(path_directory, path_project)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a style transfer experiment.")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default="~/Desktop/code/imgz_tmp/test_dir/",
        help="Path of directory to compress.",
    )
    args = parser.parse_args()

    main(args.path)
