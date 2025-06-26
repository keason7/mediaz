"""Image media class."""

import rawpy
from PIL import Image, ImageFile
from pillow_heif import register_heif_opener

from mediaz.dtype.dtype_support import DataTypesIn
from mediaz.mtype.abstract_media import AbstractMedia

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageMedia(AbstractMedia):
    """Image media class to handle image I/O and compression."""

    def __read_pil(self, path):
        """Read an image supported by PIL.

        Args:
            path (str): Input path.
        """
        register_heif_opener()
        self.media = Image.open(path)

    def __read_raw(self, path):
        """Read a RAW image.

        Args:
            path (str): Input path.
        """
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()

        self.media = Image.fromarray(rgb)

    def __write_jpg(self, path, compress_params):
        """Compress and write a JPEG image with PIL.

        Args:
            path (str): Input path.
            compress_params (dict): Compression parameters.
        """
        self.media.save(
            path,
            quality=compress_params["quality"],
            optimize=compress_params["optimize"],
            subsampling=compress_params["subsampling"],
        )

    def read(self, path):
        """Read an image file.

        Args:
            path (str): Input path.

        Raises:
            TypeError: Unknown input format.
        """
        if self.dtype_in["category"] == DataTypesIn.IMAGE_PIL.name:
            self.__read_pil(path)

        elif self.dtype_in["category"] == DataTypesIn.IMAGE_RAW.name:
            self.__read_raw(path)

        else:
            raise TypeError(f"Unknown input format. Found {self.dtype_in}.")

    def write(self, path, compress_params):
        """Compress an image and write.

        Args:
            path (str): Input path.
            compress_params (dict): Compression parameters.

        Raises:
            TypeError: Unknown output format.
        """
        if self.media.mode != "RGB":
            self.media = self.media.convert("RGB")

        if self.dtype_out["fmt"] == "JPEG":
            self.__write_jpg(path, compress_params["JPEG"])

        else:
            raise TypeError(f"Unknown output format. Found {self.dtype_out}.")
