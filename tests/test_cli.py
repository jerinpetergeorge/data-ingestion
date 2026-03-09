import pytest
from click.testing import CliRunner

from game.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def input_file(tmp_path):
    f = tmp_path / "input.txt"
    f.write_text(
        "name=levy,type=A,id=1\n"
        "name=lima,type=A,id=2\n"
        "name=john,type=A,id=3\n"
        "name=mia,type=B,id=4\n"
        "name=noah,type=B,id=5\n"
        "name=zara,type=C,id=6\n"
    )
    return str(f)


class TestCLI:
    def test_successful_run(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
            ],
        )

        assert result.exit_code == 0

    def test_output_sorted_by_hierarchy(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
            ],
        )

        lines = result.output.strip().split("\n")
        assert len(lines) == 6
        assert lines[0] == "1,levy,A"
        assert lines[1] == "2,lima,A"
        assert lines[2] == "3,john,A"
        assert lines[3] == "4,mia,B"
        assert lines[4] == "5,noah,B"
        assert lines[5] == "6,zara,C"

    def test_output_reversed_hierarchy(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "C -> B -> A",
            ],
        )

        lines = result.output.strip().split("\n")
        assert lines[0] == "6,zara,C"
        assert lines[1] == "4,mia,B"
        assert lines[2] == "5,noah,B"
        assert lines[3] == "1,levy,A"
        assert lines[4] == "2,lima,A"
        assert lines[5] == "3,john,A"

    def test_missing_keys_option_fails(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--hierarchy",
                "A -> B -> C",
            ],
        )

        assert result.exit_code != 0
        assert "Missing option" in result.output

    def test_missing_hierarchy_option_fails(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
            ],
        )

        assert result.exit_code != 0
        assert "Missing option" in result.output

    def test_missing_file_source_fails(self, runner):
        result = runner.invoke(
            main,
            [
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
            ],
        )

        assert result.exit_code != 0

    def test_short_flags(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "-k",
                "id:int,name:str,type:str",
                "-h",
                "A -> B -> C",
            ],
        )

        assert result.exit_code == 0

    def test_invalid_reader_backend_fails(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
                "--reader-backend",
                "invalid",
            ],
        )

        assert result.exit_code != 0

    def test_invalid_writer_backend_fails(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
                "--writer-backend",
                "invalid",
            ],
        )

        assert result.exit_code != 0

    def test_explicit_local_reader_backend(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
                "-r",
                "LOCAL",
            ],
        )

        assert result.exit_code == 0

    def test_rows_with_missing_keys_are_dropped(self, runner, tmp_path):
        f = tmp_path / "input.txt"
        f.write_text(
            "name=levy,type=A,id=1\n"
            "name=lima,type=A,id=2\n"
            "name=john,type=A,id=3\n"
            "name=mia,type=B,id=4\n"
            "name=noah,type=B\n"  # missing id
            "name=zara,type=C,id=6\n"
        )

        result = runner.invoke(
            main,
            [
                str(f),
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert len(lines) == 5
        assert all("noah" not in line for line in lines)

    def test_rows_with_invalid_type_are_dropped(self, runner, tmp_path):
        f = tmp_path / "input.txt"
        f.write_text(
            "name=levy,type=A,id=1\n"
            "name=lima,type=A,id=2\n"
            "name=john,type=A,id=3\n"
            "name=mia,type=B,id=4\n"
            "name=noah,type=B,id=?\n"  # id cannot be cast to int
            "name=zara,type=C,id=6\n"
        )

        result = runner.invoke(
            main,
            [
                str(f),
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
            ],
        )

        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert len(lines) == 5
        assert all("noah" not in line for line in lines)

    def test_total_row_count(self, runner, input_file):
        result = runner.invoke(
            main,
            [
                input_file,
                "--keys",
                "id:int,name:str,type:str",
                "--hierarchy",
                "A -> B -> C",
            ],
        )

        lines = result.output.strip().split("\n")
        assert len(lines) == 6
