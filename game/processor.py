from typing import Iterable

from .interface import Stage
from .models import Header


class IngestionPipeline:
    def __init__(
        self,
        rows: Iterable,
        header: Header,
        stages: list[Stage],
    ):
        self.rows = rows
        self.header = header
        self.stages = stages

    def process(self) -> Iterable[dict]:
        for row in self.rows:
            for stage in self.stages:
                row = stage.process(row)
                if not row:
                    break
            if row:
                yield row
