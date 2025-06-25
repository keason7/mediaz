"""Utils functions."""

import datetime
import logging
import logging.config

import yaml

from mediaz.dtype.dtype import get_dtype
from mediaz.dtype.dtype_support import DataTypesIn

__logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}


def read_yml(path):
    """Read YAML file.

    Args:
        path (str): Input path.

    Returns:
        dict: YAML dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yml(path, data):
    """
    Write YAML file.

    Args:
        path (str): Path of output file.
        data (dict): Dictionary to write as YAML.
    """
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f)


def get_logger(name):
    """Return logger.

    Args:
        name (str): Logger name.

    Returns:
        logging.Logger: Logger.
    """
    logging.config.dictConfig(__logger_config)
    return logging.getLogger(name)


def get_timestamp():
    """Get str timestamp.

    Returns:
        str: Timestamp in YYYY_MM_DD-HH_MM_SS format.
    """
    now = datetime.datetime.now()
    return f"{now.year:04d}_{now.month:02d}_{now.day:02d}-{now.hour:02d}_{now.minute:02d}_{now.second:02d}"


def create_project(path_in):
    """Create project directory.

    Args:
        path_in (pathlib.Path): Input directory path to compress.

    Returns:
        pathlib.Path: Output data directory path with compressed files.
        pathlib.Path: Output summary directory path with statistic file.
    """
    timestamp = get_timestamp()

    # create root output directory
    path_project = path_in.parent / f"{timestamp}_{path_in.name}"
    path_project.mkdir(mode=0o777, parents=False, exist_ok=False)

    path_data = path_project / "data"
    path_data.mkdir(mode=0o777, parents=False, exist_ok=False)

    path_summary = path_project / "summary"
    path_summary.mkdir(mode=0o777, parents=False, exist_ok=False)

    # get all nested subdirectories in input root directory
    path_in_directories = [path for path in path_in.rglob("*") if path.is_dir()]

    # create all nested directory in output root directory
    for path_directory in path_in_directories:
        path_project_directories = path_data / path_directory.relative_to(path_in)
        path_project_directories.mkdir(mode=0o777, parents=False, exist_ok=False)

    return path_data, path_summary


def sanitize_paths(path_out_files):
    """Sanitize paths to avoid same naming issues.
    Naming issue, file name should be changed to avoid following:
    /path/to/file.png -> /path/to/file.jpg
    /path/to/file.nef -> /path/to/file.jpg

    Args:
        path_out_files (list): List of output paths.

    Returns:
        list: List of sanitized output paths.
    """
    sanitized_paths, path_count = [], {}

    for path in path_out_files:
        # output exact path has no been seen
        # initialize counter in dict
        if str(path) not in path_count:
            path_count[str(path)] = 0
            sanitized_paths.append(path)

        # output path has been seen (duplicate output file path)
        # rename is necessary to avoid file overwrite and increment counter
        else:
            path_count[str(path)] += 1
            new_name = f"{path.stem} ({path_count[str(path)]}){path.suffix}"
            sanitized_paths.append(path.parent / new_name)

    return sanitized_paths


def get_files_paths(path_in, path_project, out_dtype):
    """From in and out root directory paths and out data types, get all in and associated out paths.

    Args:
        path_in (pathlib.Path): Root in directory path.
        path_project (pathlib.Path): Root out directory path.
        out_dtype (dict): Dictionary of out dtype such as:
            {'image': {'fmt': 'JPEG', 'ext': '.jpg'}, 'video': {'fmt': 'MP4', 'ext': '.mp4'}}

    Returns:
        list: List of input files paths.
        list: List of output files paths.
    """
    path_out_files = []
    path_in_files = [path for path in path_in.rglob("*") if path.is_file()]

    for path_in_file in path_in_files:
        # get input file data type
        dtype = get_dtype(DataTypesIn, ext=path_in_file.suffix)

        # /path/to/in/dir/aa.png -> /path/to/out/dir/aa.png
        path_out_file = path_project / path_in_file.relative_to(path_in)

        # prepare path for file copy, keep original ext
        if dtype is None:
            path_out_files.append(path_out_file.with_suffix(path_in_file.suffix.lower()))

        # prepare path for image file compression, replace with output ext
        elif dtype["category"] in [DataTypesIn.IMAGE_PIL.name, DataTypesIn.IMAGE_RAW.name]:
            path_out_files.append(path_out_file.with_suffix(out_dtype["image"]["ext"]))

        # prepare path for video file compression, replace with output ext
        else:
            path_out_files.append(path_out_file.with_suffix(out_dtype["video"]["ext"]))

    return path_in_files, sanitize_paths(path_out_files)


def update_stats(stats, data):
    """Update statistics dictionary.

    Args:
        stats (dict): Statistics dictionary.
        data (dict): Data dictionary.

    Returns:
        dict: Updated statistics dictionary.
    """
    for key, value in data.items():
        # stats key list is not empty, reset it
        if len(stats[key]) > 0:
            stats[key] = []
        stats[key].append(value)

    return stats


def verify_number_of_files(path_in_directory, path_out_directory):
    """Verify that two directoies have the same number of files.

    Args:
        path_in_directory (pathlib.Path): Directory path.
        path_out_directory (pathlib.Path): Directory path.

    Raises:
        ValueError: Both paths must be directories.
        ValueError: Input and output folder do not have the same number of files.
    """
    if not path_in_directory.is_dir() or not path_out_directory.is_dir():
        raise ValueError("Both paths must be directories.")

    count_in_directory = sum(1 for p in path_in_directory.glob("**/*") if p.is_file())
    count_out_directory = sum(1 for p in path_out_directory.glob("**/*") if p.is_file())

    if count_in_directory != count_out_directory:
        raise ValueError(
            "Input and output folder do not have the same number of files: "
            f"found {count_in_directory} input files and {count_out_directory} output files."
        )
