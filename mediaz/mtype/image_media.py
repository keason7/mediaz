import rawpy
from PIL import Image

from mediaz.dtype.dtype_support import DataTypesIn


class ImageMedia:
    def __init__(self, dtype_in, dtype_out):
        self.img = None
        self.dtype_in = dtype_in
        self.dtype_out = dtype_out

    def __read_pil(self, path, fmt):
        self.img = Image.open(path, formats=[fmt])

    def __read_raw(self, path):
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()

        self.img = Image.fromarray(rgb)

    def read(self, path):
        if self.dtype_in["category"] == DataTypesIn.IMAGE_PIL.name:
            self.__read_pil(path, self.dtype_in["fmt"])
        elif self.dtype_in["category"] == DataTypesIn.IMAGE_RAW.name:
            self.__read_raw(path)
        else:
            raise TypeError(f"Unknown input format. Found {self.dtype_in}.")

    def __write_jpg(self, path, compression):
        self.img.save(
            path,
            quality=compression["quality"],
            optimize=compression["optimize"],
            progressive=compression["progressive"],
            subsampling=compression["subsampling"],
        )

    def write(self, path, compression):
        if self.img.mode != "RGB":
            self.img = self.img.convert("RGB")

        if self.dtype_out["fmt"] == "JPEG":
            self.__write_jpg(path, compression["JPEG"])

        else:
            raise TypeError(f"Unknown output format. Found {self.dtype_out}.")
