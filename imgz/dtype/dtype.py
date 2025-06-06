from imgz.dtype.dtype_support import DataTypesIn
from imgz.media_type.image_media import ImageMedia


def get_dtype_from_fmt(enum, fmt):
    for category in enum:
        for dtypes_fmt, dtypes_ext in category.value.items():

            if fmt == dtypes_fmt:
                return {"category": category.name, "fmt": fmt, "ext": dtypes_ext}
    return None


def get_dtype_from_ext(enum, ext):
    for category in enum:
        for dtypes_fmt, dtypes_ext in category.value.items():

            if ext in dtypes_ext:
                return {"category": category.name, "fmt": dtypes_fmt, "ext": ext}
    return None


def get_dtype(enum, fmt=None, ext=None):
    if fmt is None and ext is None:
        raise TypeError("Invalid args, fmt and ext can't be both None.")

    if fmt is not None and ext is not None:
        raise TypeError("Invalid args, fmt and ext can't be both not None.")

    if fmt is not None:
        return get_dtype_from_fmt(enum, fmt)

    if ext is not None:
        return get_dtype_from_ext(enum, ext)


def get_media_type(path):
    ext = path.suffix.lower()
    dtype = get_dtype(DataTypesIn, ext=ext)

    if dtype is None:
        return None, None

    elif dtype["category"] == DataTypesIn.IMAGE_PIL.name:
        return ImageMedia(dtype["category"]), dtype

    else:
        return ImageMedia(dtype["category"]), dtype
