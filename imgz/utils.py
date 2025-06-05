import datetime

_out_data_types = {"JPEG": ".jpg"}


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


def get_files_paths(path_in, path_project, out_data_type):
    if out_data_type not in _out_data_types.keys():
        raise TypeError(f"Invalid output format. Available output formats: {list(_out_data_types.keys())}")

    path_in_files = [path for path in path_in.rglob("*") if path.is_file()]
    path_out_files = [
        path_project / path_in_file.relative_to(path_in).with_suffix(_out_data_types[out_data_type])
        for path_in_file in path_in_files
    ]

    return path_in_files, sanitize_paths(path_out_files)
