from unittest.mock import MagicMock

import pytest

from game.parser import IngestionParser


class TestIngestionParser:
    def _make_reader(self, rows):
        reader = MagicMock()
        reader.read.return_value = iter(rows)
        return reader

    def test_parse_single_row(self):
        reader = self._make_reader(
            [
                [
                    "name=levy",
                    "type=A",
                    "id=3",
                    "food=pizza",
                ],
            ],
        )
        parser = IngestionParser(reader)

        result = list(parser.parse())

        assert result == [
            {
                "name": "levy",
                "type": "A",
                "id": "3",
                "food": "pizza",
            },
        ]

    def test_parse_multiple_rows(self):
        reader = self._make_reader(
            [
                ["name=levy", "type=A", "id=3", "food=pizza"],
                [
                    "type=B",
                    "name=lima",
                    "noise=hello",
                    "more_noise=bye",
                    "id=?",
                    "food=fish",
                ],
            ]
        )
        parser = IngestionParser(reader)

        result = list(parser.parse())

        assert result[0] == {
            "name": "levy",
            "type": "A",
            "id": "3",
            "food": "pizza",
        }
        assert result[1] == {
            "type": "B",
            "name": "lima",
            "noise": "hello",
            "more_noise": "bye",
            "id": "?",
            "food": "fish",
        }

    def test_parse_strips_whitespace(self):
        reader = self._make_reader([["name = levy", " type = A "]])
        parser = IngestionParser(reader)

        result = list(parser.parse())

        assert result[0] == {"name": "levy", "type": "A"}

    def test_parse_empty_reader(self):
        reader = self._make_reader([])
        parser = IngestionParser(reader)

        result = list(parser.parse())

        assert result == []

    def test_parse_is_lazy_generator(self):
        reader = self._make_reader([["name=levy", "type=A"]])
        parser = IngestionParser(reader)

        import types

        assert isinstance(parser.parse(), types.GeneratorType)

    def test_parse_rows_one_at_a_time(self):
        reader = self._make_reader(
            [
                ["name=levy", "type=A"],
                ["name=lima", "type=B"],
            ]
        )
        parser = IngestionParser(reader)
        gen = parser.parse()

        assert next(gen) == {"name": "levy", "type": "A"}
        assert next(gen) == {"name": "lima", "type": "B"}
        with pytest.raises(StopIteration):
            next(gen)

    def test_parse_rows_with_different_keys(self):
        reader = self._make_reader(
            [
                ["name=levy", "type=A"],
                ["name=lima", "type=B", "noise=hello"],
            ]
        )
        parser = IngestionParser(reader)
        result = list(parser.parse())

        assert len(result[0]) == 2
        assert len(result[1]) == 3

    def test_parse_calls_reader_read(self):
        reader = self._make_reader([])
        parser = IngestionParser(reader)
        list(parser.parse())
        reader.read.assert_called_once()
