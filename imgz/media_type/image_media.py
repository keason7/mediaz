import rawpy
from PIL import Image


class ImageMedia:
    def __init__(self, category):
        self.data = None
        self.category = category

    def __read_pil(self, path, fmt):
        self.data = Image.open(path, formats=[fmt])

    def __read_raw(self, path):
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()

        self.data = Image.fromarray(rgb)

    def read(self, path, fmt):
        if self.category == "pil":
            self.__read_pil(path, fmt)
        else:
            self.__read_raw(path)

    def write(self, path, out_dtype="JPEG"):

        if self.data.mode != "RGB":
            self.data = self.data.convert("RGB")

        self.data.save(
            path,
            out_dtype,
            quality=70,
            optimize=True,
            progressive=True,
            subsampling=1,
        )
