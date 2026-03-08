import pytest

from game.errors import InvalidKeySpecError
from game.models import Header, KeySpec


class TestHeader:
    def test_from_string_single_key(self):
        header = Header.from_string("name:str")
        assert len(header.keys) == 1
        assert header.keys[0].name == "name"
        assert header.keys[0].dtype == str

    def test_from_string_multiple_keys(self):
        header = Header.from_string("id:int,name:str,score:float")
        assert len(header.keys) == 3
        assert header.keys[0] == KeySpec(name="id", dtype=int)
        assert header.keys[1] == KeySpec(name="name", dtype=str)
        assert header.keys[2] == KeySpec(name="score", dtype=float)

    def test_from_string_all_supported_types(self):
        header = Header.from_string("a:int,b:str,c:float,d:bool")
        assert header.keys[0].dtype == int
        assert header.keys[1].dtype == str
        assert header.keys[2].dtype == float
        assert header.keys[3].dtype == bool

    def test_from_string_with_whitespace(self):
        header = Header.from_string("id:int, name:str")
        assert header.keys[0].name == "id"
        assert header.keys[1].name == "name"

    def test_from_string_invalid_key_spec_raises(self):
        with pytest.raises(InvalidKeySpecError):
            Header.from_string("invalid_spec")

    def test_from_string_unsupported_type_raises(self):
        with pytest.raises(InvalidKeySpecError):
            Header.from_string("name:list")

    def test_to_keys_returns_names(self):
        header = Header.from_string("id:int,name:str,score:float")
        assert header.to_keys() == ["id", "name", "score"]

    def test_to_keys_single_key(self):
        header = Header.from_string("id:int")
        assert header.to_keys() == ["id"]

    def test_header_is_immutable(self):
        header = Header.from_string("id:int")
        with pytest.raises(Exception):
            header.keys = []

    def test_header_equality(self):
        header1 = Header.from_string("id:int,name:str")
        header2 = Header.from_string("id:int,name:str")
        assert header1 == header2

    def test_header_inequality(self):
        header1 = Header.from_string("id:int")
        header2 = Header.from_string("name:str")
        assert header1 != header2
