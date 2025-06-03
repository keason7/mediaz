from pathlib import Path

from PIL import Image

from imgz.image.image import AbstractImage

# known formats not supported by PIL
# Raster image formats
# ".heic",
# ".heif",
# ".avif",
# ".jxl",
# Vector image formats
# ".svg",
# ".pdf",
# ".ai",
# Raw image formats (camera)
# ".raw",
# ".cr2",
# ".nef",
# ".arw",
# ".dng",
# ".orf",
# ".rw2",
# Other / specialized formats
# ".exr",
# ".hdr",
# ".xcf",


_pil_formats = {
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


class StandardImage(AbstractImage):

    def read(self, path):
        self.data_type = self._get_data_type(path, _pil_formats)

        if self.data_type is not None:
            self.data = Image.open(path, formats=[self.data_type["fmt"]])

        else:
            print("Invalid ext")

    def write(self, path, filename):
        self.data.save(str(Path(path) / f"{filename}{self.data_type['ext']}"), self.data_type["fmt"])
