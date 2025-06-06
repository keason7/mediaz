from imgz.media_type.image_media import ImageMedia


_dtypes = {
    "pil": {
        "BMP": [".bmp"],
        "DDS": [".dds"],
        "DIB": [".dib"],
        "EPS": [".eps", ".ps"],
        "GIF": [".gif"],
        "ICNS": [".icns"],
        "ICO": [".ico"],
        "IM": [".im"],
        "JPEG": [".jfif", ".jpe", ".jpeg", ".jpg"],
        "JPEG2000": [".j2c", ".j2k", ".jp2", ".jpc", ".jpf", ".jpx"],
        "PCX": [".pcx"],
        "PNG": [".apng", ".png"],
        "PPM": [".pbm", ".pfm", ".pgm", ".pnm", ".ppm"],
        "SGI": [".bw", ".rgb", ".rgba", ".sgi"],
        "TGA": [".icb", ".tga", ".vda", ".vst"],
        "TIFF": [".tif", ".tiff"],
        "WEBP": [".webp"],
    },
    "raw": {
        "Generic": [".raw"],
        "Adobe": [".dng"],
        "Canon": [".cr2", ".cr3"],
        "Casio": [".bay"],
        "Fujifilm": [".raf"],
        "Hasselblad": [".3fr", ".fff"],
        "Kodak": [".k25", ".kdc"],
        "Leica": [".rwl"],
        "Nikon": [".nef", ".nrw"],
        "Olympus": [".orf"],
        "Panasonic": [".rw2"],
        "Pentax": [".pef"],
        "Phase One": [".iiq"],
        "Samsung": [".srw"],
        "Sony": [".arw", ".srf", ".sr2"],
    },
}


def get_dtype(path):
    ext = path.suffix.lower()

    for category, _ in _dtypes.items():
        for fmt, exts in _dtypes[category].items():

            if ext in exts:
                return {"category": category, "fmt": fmt, "ext": ext}
    return None


def get_media_type(path):
    dtype = get_dtype(path)

    if dtype is None:
        return None, None

    elif dtype["category"] == "pil":
        return ImageMedia(dtype["category"]), dtype

    else:
        return ImageMedia(dtype["category"]), dtype
