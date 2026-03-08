from typing import Iterable

from .interface import Writer


class StdOutWriter(Writer):
    def __init__(self, ordered_fields: list[str]):
        self.ordered_fields = ordered_fields

    def write(self, rows: Iterable[dict]) -> None:
        for row in rows:
            line = ",".join(str(row[field]) for field in self.ordered_fields)
            print(line)
