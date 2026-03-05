from dataclasses import dataclass


@dataclass(frozen=True)
class Header:
    keys: list["KeySpec"]

    @staticmethod
    def from_string(string: str) -> "Header":
        key_specs = [KeySpec.from_string(part) for part in string.split(",")]
        return Header(keys=key_specs)


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
            raise ValueError(f"Invalid key spec '{spec}'. Expected format: name:type")
        name, type_str = parts
        if type_str not in _TYPE_MAP:
            raise ValueError(f"Unsupported type '{type_str}' in spec '{spec}'")
        return KeySpec(name=name, dtype=_TYPE_MAP[type_str])
