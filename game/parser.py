from typing import Iterable

from .interface import FileReader


class IngestionParser:
    """
    Parses the input data from the reader and yields dictionaries where keys are
    derived from the header and values are the corresponding data from each row.
    """

    def __init__(self, reader: FileReader):
        self.reader = reader

    def parse(self) -> Iterable[dict]:
        for row in self.reader.read():
            dict_row = {}
            for item in row:
                key, value = item.split("=")
                dict_row[key.strip()] = value.strip()
            yield dict_row
