from typing import Iterable

from .interface import Stage


class IngestionPipeline:
    def __init__(
        self,
        rows: Iterable,
        stages: list[Stage],
    ):
        self.rows = rows
        self.stages = stages

    def process(self) -> Iterable[dict]:
        for row in self.rows:
            for stage in self.stages:
                row = stage.process(row)
                if not row:
                    break
            if row:
                yield row
