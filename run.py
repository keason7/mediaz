"""Compression entry script."""

import argparse
from pathlib import Path
from pprint import pformat

from mediaz.compress import bulk_compress
from mediaz.utils import create_project, get_logger, read_yml

logger = get_logger(__name__)


def run(path_config, no_progress_bar):
    """Compression run function.

    Args:
        path_config (str): Config YAML file path.
    """
    config = read_yml(path_config)
    logger.info("Using config:\n %s \n", pformat(config))

    path_directory = Path(config["in_path"]).expanduser()
    path_project = create_project(path_directory)

    bulk_compress(config, path_directory, path_project, no_progress_bar)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run bulk compression.")

    parser.add_argument(
        "-pc",
        "--path_config",
        type=str,
        default="./config.yml",
        help="Path of config file.",
    )

    parser.add_argument(
        "-nb",
        "--no_progress_bar",
        action="store_true",
        default=False,
        help="Enable / disable progression bar.",
    )

    args = parser.parse_args()

    run(args.path_config, args.no_progress_bar)
