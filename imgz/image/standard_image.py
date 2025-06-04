from PIL import Image

from imgz.image.image import AbstractImage

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

    def write(self, path, out_data_type="JPEG"):

        if self.data.mode != "RGB":
            self.data = self.data.convert("RGB")

        self.data.save(
            path,
            out_data_type,
            quality=70,
            optimize=True,
            progressive=True,
            subsampling=1,
        )
