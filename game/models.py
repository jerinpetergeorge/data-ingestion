from dataclasses import dataclass
from functools import cached_property

from .errors import InvalidHierarchyError, InvalidKeySpecError


@dataclass(frozen=True)
class Header:
    keys: list["KeySpec"]

    @staticmethod
    def from_string(string: str) -> "Header":
        key_specs = [KeySpec.from_string(part) for part in string.split(",")]
        return Header(keys=key_specs)

    def to_keys(self) -> list[str]:
        return [key_spec.name for key_spec in self.keys]


@dataclass(frozen=True)
class KeySpec:
    name: str
    dtype: type

    @staticmethod
    def from_string(spec: str) -> "KeySpec":
        _TYPE_MAP: dict[str, type] = {
            "int": int,
            "str": str,
            "float": float,
            "bool": bool,
        }
        parts = spec.strip().split(":")
        if len(parts) != 2:
            raise InvalidKeySpecError(
                f"Invalid key spec '{spec}'. Expected format: name:type"
            )
        name, type_str = parts
        if type_str not in _TYPE_MAP:
            msg = f"Unsupported type '{type_str}' in spec '{spec}'"
            raise InvalidKeySpecError(msg)
        return KeySpec(name=name, dtype=_TYPE_MAP[type_str])


@dataclass(frozen=True)
class Hierarchy:
    """
    Represents the ordered chain of entity types.

    e.g. "A -> B -> C" → order = ("A", "B", "C")
    """

    order: tuple[str, ...]

    @staticmethod
    def from_string(spec: str) -> "Hierarchy":
        """
        Parse "A -> B -> C" into Hierarchy(order=("A", "B", "C")).

        Raises InvalidHierarchyError if the string is malformed or
        contains cycles.
        """
        parts = [p.strip() for p in spec.split("->")]

        if len(parts) < 2:
            raise InvalidHierarchyError(
                f"Hierarchy '{spec}' must have at least two types "
                f"separated by '->'"
            )

        if any(p == "" for p in parts):
            raise InvalidHierarchyError(
                f"Hierarchy '{spec}' contains an empty type token."
            )

        if len(parts) != len(set(parts)):
            raise InvalidHierarchyError(
                f"Hierarchy '{spec}' contains a cycle or duplicate type."
            )

        return Hierarchy(order=tuple(parts))

    @cached_property
    def rank(self) -> dict[str, int]:
        """
        Returns a map of type → position. e.g. {'A': 0, 'B': 1, 'C': 2}
        """
        return {entity_type: idx for idx, entity_type in enumerate(self.order)}

    def __contains__(self, entity_type: str) -> bool:
        return entity_type in self.rank
