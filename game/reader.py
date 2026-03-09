import csv
from os import PathLike
from typing import Type

from .errors import FileReadError, ReaderBackendNotSupportedError
from .interface import FileReader


def get_reader_backend_cls(backend_type: str = "local") -> Type[FileReader]:
    """
    Get the reader backend class based on the backend type.
    """
    try:
        return READER_BACKENDS[backend_type]
    except KeyError:
        raise ReaderBackendNotSupportedError(
            f"Unsupported reader backend: {backend_type}",
        )


class LocalCSVLazyReader(FileReader):
    """
    Load file from the local disk, and read it lazily using a generator.
    """

    def __init__(self, path: str | PathLike):
        self.path = path

    def read(self):
        try:
            with open(self.path) as fp:
                reader = csv.reader(fp)
                for row in reader:
                    yield row
        except FileNotFoundError:
            raise FileReadError(f"File not found: {self.path}")


class URLFileReader(FileReader):
    """
    Load file from a URL
    """


class S3FileReader(URLFileReader):
    """
    Load file from S3
    """


# ------------------------------------------ #
# -------- Reader Backend Mappings --------- #
# ------------------------------------------ #

READER_BACKENDS = {
    "local": LocalCSVLazyReader,
    "https": URLFileReader,
    "s3": S3FileReader,
}
