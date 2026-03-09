from typing import Iterable

from game.errors import UnknownEntityTypeError

from .models import Hierarchy


class HierarchySorter:
    """
    Class responsible for ordering rows by their entity type.
    It depends on Hierarchy abstraction, not on raw strings.

    Consumes the full iterator into memory (required for sorting),
    then yields rows in hierarchy order.

    Raises UnknownEntityTypeError if a row's type is not in the declared
    hierarchy.
    """

    TYPE_KEY = "type"

    def __init__(self, hierarchy: Hierarchy) -> None:
        self.hierarchy = hierarchy

    def sort(self, rows: Iterable[dict]) -> Iterable[dict]:
        """
        Collect all rows, validate their types, then yield in hierarchy order.
        """
        collected = list(rows)

        self._validate_types(collected)

        yield from sorted(
            collected,
            key=lambda row: self.hierarchy.rank[row[self.TYPE_KEY]],
        )

    def _validate_types(self, rows: list[dict]) -> None:
        for row in rows:
            entity_type = row.get(self.TYPE_KEY)
            if entity_type not in self.hierarchy:
                raise UnknownEntityTypeError(
                    f"Entity type '{entity_type}' is not declared in "
                    f"the hierarchy. Expected one of: {self.hierarchy.order}"
                )
