import rawpy
from PIL import Image

from mediaz.dtype.dtype_support import DataTypesIn


class ImageMedia:
    def __init__(self, category):
        self.img = None
        self.category = category

    def __read_pil(self, path, fmt):
        self.img = Image.open(path, formats=[fmt])

    def __read_raw(self, path):
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()

        self.img = Image.fromarray(rgb)

    def read(self, path, fmt):
        if self.category == DataTypesIn.IMAGE_PIL.name:
            self.__read_pil(path, fmt)
        else:
            self.__read_raw(path)

    def write(self, path):
        if self.img.mode != "RGB":
            self.img = self.img.convert("RGB")

        self.img.save(
            path,
            quality=70,
            optimize=True,
            progressive=True,
            subsampling=1,
        )
