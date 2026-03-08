from dataclasses import dataclass

from .errors import InvalidKeySpecError


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
