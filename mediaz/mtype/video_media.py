"""Video media class."""

import ffmpeg

from mediaz.dtype.dtype_support import DataTypesIn
from mediaz.mtype.abstract_media import AbstractMedia


class VideoMedia(AbstractMedia):
    """Video media class to handle image I/O and compression."""

    def __read_ffmpeg(self, path):
        """Read a video supported by ffmpeg.

        Args:
            path (str): Input path.
        """
        self.media = ffmpeg.input(path)

    def __write_mp4(self, path, compress_params):
        """Compress and write a MP4 video with ffmpeg.

        Args:
            path (str): Input path.
            compress_params (dict): Compression parameters.
        """
        self.media.output(
            path,
            vcodec=compress_params["vcodec"],
            crf=compress_params["crf"],
            pix_fmt=compress_params["pix_fmt"],
            preset=compress_params["preset"],
            acodec=compress_params["acodec"],
            audio_bitrate=compress_params["audio_bitrate"],
            loglevel=compress_params["loglevel"],
            **{"x265-params": compress_params["libx265_loglevel"]},
        ).run()

    def read(self, path):
        """Read a video file.

        Args:
            path (str): Input path.

        Raises:
            TypeError: Unknown input format.
        """
        if self.dtype_in["category"] == DataTypesIn.VIDEO_FFMPEG.name:
            self.__read_ffmpeg(path)

        else:
            raise TypeError(f"Unknown input format. Found {self.dtype_in}.")

    def write(self, path, compress_params):
        """Compress a video and write.

        Args:
            path (str): Input path.
            compress_params (dict): Compression parameters.

        Raises:
            TypeError: Unknown input format.
        """
        if self.dtype_out["fmt"] == "MP4":
            self.__write_mp4(path, compress_params["MP4"])

        else:
            raise TypeError(f"Unknown output format. Found {self.dtype_out}.")
