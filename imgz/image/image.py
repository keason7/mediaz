from abc import ABC, abstractmethod
from pathlib import Path


class AbstractImage(ABC):
    def __init__(self):
        self.data = None
        self.data_type = None

    @abstractmethod
    def read(self, path):
        raise NotImplementedError("Method is not implemented.")

    def _get_data_type(self, path, fmts):
        ext = Path(path).suffix.lower()

        for fmt, exts in fmts.items():
            if ext in exts:
                return {"fmt": fmt, "ext": ext}

        return None
