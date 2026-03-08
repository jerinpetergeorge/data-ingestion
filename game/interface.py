import csv
from abc import ABC, abstractmethod
from typing import Iterable


class FileReader(ABC):
    """
    Interface for reading files. Implementations can read from various sources such as local disk, S3, etc.
    The read method should return an iterable (e.g., generator) that yields rows of data.
    """

    @abstractmethod
    def read(self) -> Iterable:
        pass


class Stage(ABC):
    """
    Interface for processing stages in the ingestion pipeline. Implementations can define specific processing logic.
    The process method should take an iterable of rows and return an iterable of processed rows.
    """

    @abstractmethod
    def process(self, rows: Iterable[dict]) -> dict | None:
        pass


class Writer(ABC):
    """
    Interface for writing processed data. Implementations can be written to various destinations
    such as stdout, files, databases, etc.
    """

    @abstractmethod
    def write(self, rows: Iterable[dict]) -> None:
        pass
