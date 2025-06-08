import argparse
from pathlib import Path

from mediaz.compress import bulk_compress
from mediaz.utils import create_project


def main(path_directory):
    path_directory = Path(path_directory).expanduser()
    path_project = create_project(path_directory)

    _out_dtypes = {
        "image": {"fmt": "JPEG", "ext": ".jpg"},
        "video": {"fmt": "MP4", "ext": ".mp4"},
    }
    bulk_compress(path_directory, path_project, _out_dtypes)


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
