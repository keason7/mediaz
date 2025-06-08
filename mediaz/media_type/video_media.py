import ffmpeg


class VideoMedia:
    def __init__(self, category):
        self.frames = None
        self.category = category

    def read(self, path, fmt):
        self.frames = ffmpeg.input(path)

    def write(self, path):
        self.frames.output(
            path,
            loglevel="quiet",
            **{"x265-params": "log-level=quiet"},
            vcodec="libx265",
            crf=28,
            pix_fmt="yuv420p10le",
            preset="fast",
            acodec="libopus",
            audio_bitrate="96k",
        ).run()
