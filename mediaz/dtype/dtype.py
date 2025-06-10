"""Data types functions."""

from mediaz.dtype.dtype_support import DataTypesIn, DataTypesOut
from mediaz.mtype.image_media import ImageMedia
from mediaz.mtype.video_media import VideoMedia


def get_dtype_from_fmt(enum, fmt):
    """Get data type from format.

    Args:
        enum (enum.Enum): Datatype Enum.
        fmt (str): Format string.

    Returns:
        dict or None: Return Enum data type dict if fmt is matched, else None.
    """
    for category in enum:
        for dtypes_fmt, dtypes_ext in category.value.items():
            if fmt == dtypes_fmt:
                return {"category": category.name, "fmt": fmt, "ext": dtypes_ext}
    return None


def get_dtype_from_ext(enum, ext):
    """Get data type from extention.

    Args:
        enum (enum.Enum): Datatype Enum.
        ext (str): Extention string.

    Returns:
        dict or None: Return Enum data type dict if ext is matched, else None.
    """
    for category in enum:
        for dtypes_fmt, dtypes_ext in category.value.items():
            if ext.lower() in dtypes_ext:
                return {"category": category.name, "fmt": dtypes_fmt, "ext": ext.lower()}
    return None


def get_dtype(enum, fmt=None, ext=None):
    """From format string or extention string, get data type.

    Args:
        enum (enum.Enum): Datatype Enum.
        fmt (str or None, optional): Format string. Defaults to None.
        ext (str or None, optional): Extention string. Defaults to None.

    Raises:
        TypeError: Invalid args, fmt and ext can't be both None.
        TypeError: Invalid args, fmt and ext can't be both not None.

    Returns:
        dict or None: Data type dictionary or None.
    """
    if fmt is None and ext is None:
        raise TypeError("Invalid args, fmt and ext can't be both None.")

    if fmt is not None and ext is not None:
        raise TypeError("Invalid args, fmt and ext can't be both not None.")

    if fmt is not None:
        return get_dtype_from_fmt(enum, fmt)

    if ext is not None:
        return get_dtype_from_ext(enum, ext)


def get_media_obj(path_in, path_out):
    """Evaluate input and output datatype, and return appropriate media object.

    Args:
        path_in (pathlib.Path): Input file path.
        path_out (pathlib.Path): Output file path.

    Returns:
        ImageMedia or VideoMedia or None: None or appropriate media object.
    """
    # get data type from file extention
    dtype_in = get_dtype(DataTypesIn, ext=path_in.suffix.lower())
    dtype_out = get_dtype(DataTypesOut, ext=path_out.suffix.lower())

    # unknown data type
    if dtype_in is None:
        return None

    # image file
    elif dtype_in["category"] in [DataTypesIn.IMAGE_PIL.name, DataTypesIn.IMAGE_RAW.name]:
        return ImageMedia(dtype_in, dtype_out)

    # video file
    else:
        return VideoMedia(dtype_in, dtype_out)
