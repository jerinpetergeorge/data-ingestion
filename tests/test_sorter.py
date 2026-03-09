import pytest

from game.errors import UnknownEntityTypeError
from game.models import Hierarchy
from game.sorter import HierarchySorter


class TestHierarchySorter:
    def test_sorts_rows_by_hierarchy_order(self):
        hierarchy = Hierarchy.from_string("A -> B -> C")
        sorter = HierarchySorter(hierarchy)
        rows = [
            {"type": "C", "name": "lima"},
            {"type": "A", "name": "levy"},
            {"type": "B", "name": "john"},
        ]

        result = list(sorter.sort(rows))

        assert [r["type"] for r in result] == ["A", "B", "C"]

    def test_preserves_row_data_after_sorting(self):
        hierarchy = Hierarchy.from_string("A -> B")
        sorter = HierarchySorter(hierarchy)
        rows = [
            {"type": "B", "name": "lima", "id": 2},
            {"type": "A", "name": "levy", "id": 1},
        ]

        result = list(sorter.sort(rows))

        assert result[0] == {"type": "A", "name": "levy", "id": 1}
        assert result[1] == {"type": "B", "name": "lima", "id": 2}

    def test_multiple_rows_same_type(self):
        hierarchy = Hierarchy.from_string("A -> B -> C")
        sorter = HierarchySorter(hierarchy)
        rows = [
            {"type": "B", "name": "first"},
            {"type": "A", "name": "second"},
            {"type": "B", "name": "third"},
        ]

        result = list(sorter.sort(rows))

        assert result[0]["type"] == "A"
        assert result[1]["type"] == "B"
        assert result[2]["type"] == "B"

    def test_already_sorted_rows_unchanged(self):
        hierarchy = Hierarchy.from_string("A -> B -> C")
        sorter = HierarchySorter(hierarchy)
        rows = [
            {"type": "A", "name": "levy"},
            {"type": "B", "name": "lima"},
            {"type": "C", "name": "john"},
        ]

        result = list(sorter.sort(rows))

        assert [r["type"] for r in result] == ["A", "B", "C"]

    def test_empty_rows_yields_nothing(self):
        hierarchy = Hierarchy.from_string("A -> B -> C")
        sorter = HierarchySorter(hierarchy)

        result = list(sorter.sort([]))

        assert result == []

    def test_raises_on_unknown_entity_type(self):
        hierarchy = Hierarchy.from_string("A -> B -> C")
        sorter = HierarchySorter(hierarchy)
        rows = [{"type": "Z", "name": "levy"}]

        with pytest.raises(UnknownEntityTypeError, match="Z"):
            list(sorter.sort(rows))

    def test_raises_on_missing_type_key(self):
        hierarchy = Hierarchy.from_string("A -> B")
        sorter = HierarchySorter(hierarchy)
        rows = [{"name": "levy"}]

        with pytest.raises(UnknownEntityTypeError):
            list(sorter.sort(rows))

    def test_raises_before_yielding_any_rows(self):
        hierarchy = Hierarchy.from_string("A -> B")
        sorter = HierarchySorter(hierarchy)
        rows = [
            {"type": "A", "name": "levy"},
            {"type": "Z", "name": "unknown"},
        ]

        with pytest.raises(UnknownEntityTypeError):
            list(sorter.sort(rows))
