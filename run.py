"""Compression entry script."""

import argparse
from pathlib import Path

from mediaz.compress import bulk_compress
from mediaz.utils import create_project, read_yml


def run(path_config):
    """Compression run function.

    Args:
        path_config (str): Config YAML file path.
    """
    config = read_yml(path_config)

    path_directory = Path(config["in_path"]).expanduser()
    path_project = create_project(path_directory)

    bulk_compress(path_directory, path_project, config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run bulk compression.")
    parser.add_argument(
        "-pc",
        "--path_config",
        type=str,
        default="./config.yml",
        help="Path of config file.",
    )
    args = parser.parse_args()

    run(args.path_config)
