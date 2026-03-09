import enum
from typing import Iterable

from .errors import WriterBackendNotSupportedError
from .interface import Writer
from .mixins import EnumChoiceMixin


def get_writer_backend_cls(backend_type: str) -> type[Writer]:
    """
    Get the writer backend class based on the backend type.
    """
    try:
        return WriterBackend[backend_type].value
    except KeyError:
        raise WriterBackendNotSupportedError(
            f"Unsupported writer backend: {backend_type}"
        )


class StdOutWriter(Writer):
    """
    Write rows to standard output.
    """

    def __init__(self, ordered_fields: list[str]):
        self.ordered_fields = ordered_fields

    def write(self, rows: Iterable[dict]) -> None:
        for row in rows:
            line = ",".join(str(row[field]) for field in self.ordered_fields)
            print(line)


class CSVWriter(Writer):
    """
    Write rows to a CSV file.
    """


# ------------------------------------------ #
# -------- Writer Backend Mappings --------- #
# ------------------------------------------ #


class WriterBackend(EnumChoiceMixin, enum.Enum):
    """
    Enum for supported writer backends. The value of each member is
    the corresponding writer class.
    """

    STDOUT = StdOutWriter
    CSV = CSVWriter
