import rawpy
from PIL import Image

from imgz.image.image import AbstractImage

_raw_formats = {
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


class RawImage(AbstractImage):

    def read(self, path):
        self.data_type = self._get_data_type(path, _raw_formats)

        if self.data_type is not None:
            with rawpy.imread(path) as raw:
                rgb = raw.postprocess()

            self.data = Image.fromarray(rgb)

        else:
            print("Invalid ext")

    def write(self, path, filename):
        pass
