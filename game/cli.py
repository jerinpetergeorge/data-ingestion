import click

from .models import Header
from .parser import IngestionParser
from .processor import IngestionPipeline
from .reader import READER_BACKENDS, get_reader_backend_cls
from .stages import RequiredKeysFilter, TypeChecker
from .writer import StdOutWriter


@click.command()
@click.argument("file_source")
@click.option(
    "--keys",
    "header_string",
    required=True,
    help="Keys spec e.g. 'id:int,name:str,type:str'",
)
@click.option(
    "--hierarchy",
    "hierarchy_string",
    required=True,
    help="Output hierarchy specification. Example: A -> B -> C",
)
@click.option(
    "--reader-backend",
    "-r",
    type=click.Choice(list(READER_BACKENDS.keys())),
    default=None,
    help="Force a specific reader backend. Auto-detected if not set.",
)
def main(
    file_source: str,
    header_string: str,
    hierarchy_string: str,
    reader_backend: str | None,
):
    """Read a key=value CSV file and output filtered, typed rows to stdout."""
    reader = get_reader_backend_cls(reader_backend)(file_source)
    header = Header.from_string(header_string)
    pipeline = IngestionPipeline(
        rows=IngestionParser(reader).parse(),
        stages=[
            RequiredKeysFilter(header),
            TypeChecker(header),
        ],
    )
    StdOutWriter(header.to_keys()).write(rows=pipeline.process())


if __name__ == "__main__":
    main()
