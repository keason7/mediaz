import datetime
from pathlib import Path


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
    path_count = {}

    new_path_out = []

    for path in path_out_files:
        path = Path(path)

        stem, suffix = path.stem, path.suffix
        parent = path.parent

        if str(path) not in path_count:
            new_path_out.append(str(path))
            path_count[str(path)] = 0
        else:
            path_count[str(path)] += 1
            new_name = f"{stem} ({path_count[str(path)]}){suffix}"
            new_path_out.append(str(parent / new_name))

    return new_path_out
