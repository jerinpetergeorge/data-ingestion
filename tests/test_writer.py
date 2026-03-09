import pytest

from game.errors import WriterBackendNotSupportedError
from game.writer import CSVWriter, StdOutWriter, get_writer_backend_cls


class TestStdOutWriter:
    def test_writes_single_row(self, capsys):
        writer = StdOutWriter(ordered_fields=["name", "type", "id", "food"])
        writer.write([{"name": "levy", "type": "A", "id": 3, "food": "pizza"}])

        assert capsys.readouterr().out == "levy,A,3,pizza\n"

    def test_writes_multiple_rows(self, capsys):
        writer = StdOutWriter(ordered_fields=["name", "id"])
        writer.write(
            [
                {"name": "levy", "id": 3},
                {"name": "lima", "id": 4},
            ]
        )

        output = capsys.readouterr().out
        assert output == "levy,3\nlima,4\n"

    def test_respects_field_order(self, capsys):
        writer = StdOutWriter(ordered_fields=["id", "food", "name"])
        writer.write([{"name": "levy", "type": "A", "id": 3, "food": "pizza"}])

        assert capsys.readouterr().out == "3,pizza,levy\n"

    def test_strips_noise_keys(self, capsys):
        writer = StdOutWriter(ordered_fields=["name", "id"])
        writer.write(
            [
                {
                    "name": "lima",
                    "id": 4,
                    "noise": "hello",
                    "more_noise": "bye",
                },
            ],
        )

        assert capsys.readouterr().out == "lima,4\n"

    def test_empty_rows_writes_nothing(self, capsys):
        writer = StdOutWriter(ordered_fields=["name", "id"])
        writer.write([])

        assert capsys.readouterr().out == ""

    def test_write_returns_none(self):
        writer = StdOutWriter(ordered_fields=["name"])
        result = writer.write([{"name": "levy"}])

        assert result is None


class TestGetWriterBackendCls:
    @pytest.mark.parametrize(
        "backend_type, expected_cls",
        [
            ("STDOUT", StdOutWriter),
            ("CSV", CSVWriter),
        ],
    )
    def test_returns_correct_writer_class(self, backend_type, expected_cls):
        assert get_writer_backend_cls(backend_type) is expected_cls

    @pytest.mark.parametrize(
        "backend_type",
        [
            "invalid",
            "",
            "stdout",
            "file",
        ],
    )
    def test_raises_on_unsupported_backend(self, backend_type):
        with pytest.raises(WriterBackendNotSupportedError):
            get_writer_backend_cls(backend_type)

    def test_raises_with_correct_message(self):
        with pytest.raises(
            WriterBackendNotSupportedError,
            match="Unsupported writer backend: invalid",
        ):
            get_writer_backend_cls("invalid")

    def test_returns_a_class_not_an_instance(self):
        result = get_writer_backend_cls("STDOUT")

        assert isinstance(result, type)
