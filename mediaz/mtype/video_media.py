import ffmpeg

from mediaz.dtype.dtype_support import DataTypesIn


class VideoMedia:
    def __init__(self, dtype_in, dtype_out):
        self.frames = None
        self.dtype_in = dtype_in
        self.dtype_out = dtype_out

    def __read_ffmpeg(self, path):
        self.frames = ffmpeg.input(path)

    def read(self, path):
        if self.dtype_in["category"] == DataTypesIn.VIDEO_FFMPEG.name:
            self.__read_ffmpeg(path)
        else:
            raise TypeError(f"Unknown input format. Found {self.dtype_in}.")

    def __write_mp4(self, path, compression):
        self.frames.output(
            path,
            vcodec=compression["vcodec"],
            crf=compression["crf"],
            pix_fmt=compression["pix_fmt"],
            preset=compression["preset"],
            acodec=compression["acodec"],
            audio_bitrate=compression["audio_bitrate"],
            loglevel=compression["loglevel"],
            **{"x265-params": compression["libx265_loglevel"]},
        ).run()

    def write(self, path, compression):
        if self.dtype_out["fmt"] == "MP4":
            self.__write_mp4(path, compression["MP4"])

        else:
            raise TypeError(f"Unknown output format. Found {self.dtype_out}.")
