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
