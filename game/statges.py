from .interface import Stage
from .models import Header


class TypeChecker(Stage):
    """
    A stage that checks if the types of the values in the row match the expected types defined in the header.
    If a value does not match the expected type, it raises a ValueError.
    """

    def __init__(self, header: Header):
        self.header = header

    def process(self, row: dict) -> dict | None:
        for key_spec in self.header.keys:
            try:
                key_spec.dtype(row[key_spec.name])
            except ValueError:
                return None
        return row


class RequiredKeysFilter(Stage):
    """
    A stage that filters out rows that do not contain all required keys.
    """

    def __init__(self, keys: list[str]):
        self.keys = keys

    def process(self, row: dict) -> dict | None:
        try:
            return {key: row[key] for key in self.keys}
        except KeyError:
            return None
