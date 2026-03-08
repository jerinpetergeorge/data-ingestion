from .interface import Stage
from .models import Header


class TypeChecker(Stage):
    """
    Validates and casts row values to their declared types.
    Drops the row if any value cannot be cast.
    If a value does not match the expected type, it raises a ValueError.
    """

    def __init__(self, header: Header):
        self.header = header

    def process(self, row: dict) -> dict | None:
        for key_spec in self.header.keys:
            try:
                row[key_spec.name] = key_spec.dtype(row[key_spec.name])
            except ValueError:
                return None
        return row


class RequiredKeysFilter(Stage):
    """
    Filters out rows missing any required key.
    As a side effect, strips noise keys and only important keys are returned.
    """

    def __init__(self, header: Header):
        self.header = header
        self.keys = header.to_keys()

    def process(self, row: dict) -> dict | None:
        try:
            return {key: row[key] for key in self.keys}
        except KeyError:
            return None
