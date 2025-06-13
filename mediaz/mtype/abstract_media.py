"""Abstract media class."""

from abc import ABC, abstractmethod


class AbstractMedia(ABC):
    """Abstract media class for specific medias classes."""

    def __init__(self, dtype_in, dtype_out):
        """Initialize object.

        Args:
            dtype_in (dict): Input data type dict.
            dtype_out (dict): Output data type dict.
        """
        self.media = None
        self.dtype_in = dtype_in
        self.dtype_out = dtype_out

    @abstractmethod
    def read(self, path):
        """Read a media file.

        Args:
            path (str): Input file path.

        Raises:
            NotImplementedError: Method is not implemented is abstract class.
        """
        raise NotImplementedError("Method is not implemented is abstract class.")

    @abstractmethod
    def write(self, path, compress_params):
        """Write and compress a media file.

        Args:
            path (str): Output file path.
            compress_params (dict): Compression parameters.

        Raises:
            NotImplementedError: Method is not implemented is abstract class.
        """
        raise NotImplementedError("Method is not implemented is abstract class.")
