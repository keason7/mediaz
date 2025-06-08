import datetime

from mediaz.dtype.dtype import get_dtype
from mediaz.dtype.dtype_support import DataTypesIn, DataTypesOut


def get_timestamp():
    now = datetime.datetime.now()
    return f"{now.year:04d}_{now.month:02d}_{now.day:02d}-{now.hour:02d}_{now.minute:02d}_{now.second:02d}"


def create_project(path_in):
    timestamp = get_timestamp()

    path_project = path_in.parent / f"{timestamp}_{path_in.name}"
    path_project.mkdir(mode=0o777, parents=False, exist_ok=False)

    path_in_directories = [path for path in path_in.rglob("*") if path.is_dir()]

    for path_directory in path_in_directories:
        path_project_directories = path_project / path_directory.relative_to(path_in)
        path_project_directories.mkdir(mode=0o777, parents=False, exist_ok=False)

    return str(path_project)


def sanitize_paths(path_out_files):
    path_out_files_sanitized = []
    path_count = {}

    for path in path_out_files:
        if str(path) not in path_count:
            path_count[str(path)] = 0
            path_out_files_sanitized.append(str(path))
        else:
            path_count[str(path)] += 1
            new_name = f"{path.stem} ({path_count[str(path)]}){path.suffix}"
            path_out_files_sanitized.append(str(path.parent / new_name))

    return path_out_files_sanitized


def get_files_paths(path_in, path_project, out_dtype):
    for _, dtype in out_dtype.items():
        if dtype["fmt"] not in DataTypesOut.keys():
            raise TypeError(f"Invalid output format. Available output formats: {list(DataTypesOut.keys())}")

    path_in_files = [path for path in path_in.rglob("*") if path.is_file()]
    path_out_files = []

    for path_in_file in path_in_files:

        dtype = get_dtype(DataTypesIn, ext=path_in_file.suffix)

        if dtype is None:
            path_out_files.append(
                path_project / path_in_file.relative_to(path_in).with_suffix(path_in_file.suffix.lower())
            )

        elif dtype["category"] in [DataTypesIn.IMAGE_PIL.name, DataTypesIn.IMAGE_RAW.name]:
            path_out_files.append(
                path_project / path_in_file.relative_to(path_in).with_suffix(out_dtype["image"]["ext"])
            )

        else:
            path_out_files.append(
                path_project / path_in_file.relative_to(path_in).with_suffix(out_dtype["video"]["ext"])
            )

    return path_in_files, sanitize_paths(path_out_files)
