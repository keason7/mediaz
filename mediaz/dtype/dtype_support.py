"""Supported data types Enums."""

from enum import Enum


class DataTypesIn(Enum):
    """Input supported data types."""

    IMAGE_PIL = {
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
    }

    IMAGE_RAW = {
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
    }

    VIDEO_FFMPEG = {
        "MP4": [".mp4"],
        "MPEG": [".mpg", ".mpeg"],
        "AVI": [".avi"],
        "MKV": [".mkv"],
        "MOV": [".mov"],
        "WMV": [".wmv"],
        "FLV": [".flv"],
        "WebM": [".webm"],
        "OGG": [".ogv", ".ogg"],
        "3GP": [".3gp"],
        "MTS": [".mts", ".m2ts"],
    }


class DataTypesOut(Enum):
    """Output supported data types."""

    IMAGE_JPEG = {"JPEG": ".jpg"}
    VIDEO_MP4 = {"MP4": ".mp4"}

    @classmethod
    def keys(cls):
        """Get members keys.

        Args:
            cls (enum.EnumType): _description_

        Returns:
            list: List containing keys for each Enum member dictionary.
        """
        return [key for member in cls for key in member.value.keys()]

    @classmethod
    def values(cls):
        """Get members values.

        Args:
            cls (enum.EnumType): _description_

        Returns:
            list: List containing values for each Enum member dictionary.
        """
        return [value for member in cls for value in member.value.values()]
