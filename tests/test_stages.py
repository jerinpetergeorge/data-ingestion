from game.models import Header
from game.stages import RequiredKeysFilter, TypeChecker


class TestTypeChecker:
    def test_casts_string_to_int(self):
        checker = TypeChecker(Header.from_string("id:int"))
        result = checker.process({"id": "3"})
        assert result == {"id": 3}

    def test_casts_string_to_float(self):
        checker = TypeChecker(Header.from_string("score:float"))
        result = checker.process({"score": "3.14"})
        assert result == {"score": 3.14}

    def test_casts_string_to_bool(self):
        checker = TypeChecker(Header.from_string("active:bool"))
        result = checker.process({"active": "True"})
        assert result == {"active": True}

    def test_casts_multiple_keys(self):
        checker = TypeChecker(
            Header.from_string(
                "id:int,name:str,score:float",
            ),
        )
        result = checker.process({"id": "3", "name": "levy", "score": "9.5"})
        assert result == {"id": 3, "name": "levy", "score": 9.5}

    def test_returns_none_on_invalid_cast(self):
        checker = TypeChecker(Header.from_string("id:int"))
        result = checker.process({"id": "?"})
        assert result is None

    def test_returns_none_if_any_key_fails(self):
        checker = TypeChecker(Header.from_string("id:int,score:float"))
        result = checker.process({"id": "3", "score": "not_a_float"})
        assert result is None

    def test_passes_through_already_correct_type(self):
        checker = TypeChecker(Header.from_string("id:int"))
        result = checker.process({"id": 3})
        assert result == {"id": 3}

    def test_preserves_extra_keys_in_row(self):
        checker = TypeChecker(Header.from_string("id:int"))
        result = checker.process({"id": "3", "noise": "extra"})
        assert result["noise"] == "extra"


class TestRequiredKeysFilter:
    def test_returns_only_required_keys(self):
        f = RequiredKeysFilter(
            Header.from_string(
                "name:str,type:str,id:str,food:str",
            ),
        )
        result = f.process(
            {
                "name": "levy",
                "type": "A",
                "id": "3",
                "food": "pizza",
                "noise": "extra",
            }
        )
        assert result == {
            "name": "levy",
            "type": "A",
            "id": "3",
            "food": "pizza",
        }
        assert "noise" not in result

    def test_strips_noise_keys(self):
        f = RequiredKeysFilter(Header.from_string("name:str,id:str"))
        result = f.process(
            {"name": "lima", "id": "1", "noise": "hello", "more_noise": "bye"}
        )
        assert set(result.keys()) == {"name", "id"}

    def test_returns_none_on_missing_required_key(self):
        f = RequiredKeysFilter(Header.from_string("name:str,id:str,food:str"))
        result = f.process({"name": "levy", "food": "pizza"})
        assert result is None

    def test_returns_none_if_all_keys_missing(self):
        f = RequiredKeysFilter(Header.from_string("name:str,id:str"))
        result = f.process({})
        assert result is None

    def test_exact_keys_match_passes(self):
        f = RequiredKeysFilter(Header.from_string("name:str,type:str"))
        result = f.process({"name": "levy", "type": "A"})
        assert result == {"name": "levy", "type": "A"}

    def test_preserves_key_order_from_header(self):
        f = RequiredKeysFilter(Header.from_string("id:str,food:str,name:str"))
        result = f.process({"food": "pizza", "name": "levy", "id": "3"})
        assert list(result.keys()) == [
            "id",
            "food",
            "name",
        ]
