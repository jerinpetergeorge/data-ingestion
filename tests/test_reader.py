import pytest

from game.errors import FileReadError, ReaderBackendNotSupportedError
from game.reader import (
    LocalCSVLazyReader,
    S3FileReader,
    URLFileReader,
    get_reader_backend_cls,
)


class TestLocalCSVLazyReader:
    def test_init_stores_path(self):
        reader = LocalCSVLazyReader("data.csv")
        assert reader.path == "data.csv"

    def test_init_accepts_pathlike(self, tmp_path):
        path = tmp_path / "data.csv"
        reader = LocalCSVLazyReader(path)
        assert reader.path == path

    def test_read_yields_rows(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name=levy,type=A,id=3,food=pizza\n")

        reader = LocalCSVLazyReader(csv_file)
        rows = list(reader.read())

        assert rows == [["name=levy", "type=A", "id=3", "food=pizza"]]

    def test_read_is_lazy_generator(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name=levy,type=A,id=3,food=pizza\n")

        reader = LocalCSVLazyReader(csv_file)

        import types

        assert isinstance(reader.read(), types.GeneratorType)

    def test_read_multiple_rows(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text(
            "name=levy,type=A,id=3,food=pizza\n"
            "type=B,name=lima,noise=hello,more_noise=bye,id=?,food=fish\n"
        )

        reader = LocalCSVLazyReader(csv_file)
        rows = list(reader.read())

        assert rows[0] == ["name=levy", "type=A", "id=3", "food=pizza"]
        assert rows[1] == [
            "type=B",
            "name=lima",
            "noise=hello",
            "more_noise=bye",
            "id=?",
            "food=fish",
        ]

    def test_read_rows_can_have_different_keys(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text(
            "name=levy,type=A,id=3,food=pizza\n"
            "type=B,name=lima,noise=hello,more_noise=bye,id=?,food=fish\n"
        )

        reader = LocalCSVLazyReader(csv_file)
        rows = list(reader.read())

        assert len(rows[0]) == 4
        assert len(rows[1]) == 6

    def test_read_empty_file(self, tmp_path):
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")

        reader = LocalCSVLazyReader(csv_file)
        assert list(reader.read()) == []

    def test_read_rows_one_at_a_time(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text(
            "name=levy,type=A,id=3,food=pizza\n"
            "type=B,name=lima,noise=hello,more_noise=bye,id=?,food=fish\n"
        )

        reader = LocalCSVLazyReader(csv_file)
        gen = reader.read()

        assert next(gen) == ["name=levy", "type=A", "id=3", "food=pizza"]
        assert next(gen) == [
            "type=B",
            "name=lima",
            "noise=hello",
            "more_noise=bye",
            "id=?",
            "food=fish",
        ]
        with pytest.raises(StopIteration):
            next(gen)

    def test_read_file_not_found_raises(self):
        reader = LocalCSVLazyReader("nonexistent.csv")

        with pytest.raises(
            FileReadError,
            match="File not found: nonexistent.csv",
        ):
            list(reader.read())


class TestGetReaderBackendCls:
    @pytest.mark.parametrize(
        "backend_type, expected_cls",
        [
            ("LOCAL", LocalCSVLazyReader),
            ("S3", S3FileReader),
            ("URL", URLFileReader),
        ],
    )
    def test_returns_correct_reader_class(self, backend_type, expected_cls):
        assert get_reader_backend_cls(backend_type) is expected_cls

    @pytest.mark.parametrize(
        "backend_type",
        [
            "invalid",
            "",
            "local",  # case-sensitive
            "ftp",
        ],
    )
    def test_raises_on_unsupported_backend(self, backend_type):
        with pytest.raises(ReaderBackendNotSupportedError):
            get_reader_backend_cls(backend_type)

    def test_raises_with_correct_message(self):
        with pytest.raises(
            ReaderBackendNotSupportedError,
            match="Unsupported reader backend: invalid",
        ):
            get_reader_backend_cls("invalid")

    def test_returns_a_class_not_an_instance(self):
        result = get_reader_backend_cls("LOCAL")

        assert isinstance(result, type)
