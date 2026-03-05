import csv
from os import PathLike

from .interface import FileReader


class LocalCSVLazyReader(FileReader):
    """
    Load file from the local disk, and read it lazily using a generator.
    """

    def __init__(self, path: str | PathLike):
        self.path = path

    def read(self):
        with open(self.path) as fp:
            reader = csv.reader(fp)
            for row in reader:
                yield row


class S3FileReader(FileReader):
    """
    Load file from S3
    """
