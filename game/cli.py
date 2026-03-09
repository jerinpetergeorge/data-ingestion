import click

from .models import Header, Hierarchy
from .parser import IngestionParser
from .processor import IngestionPipeline
from .reader import ReaderBackend, get_reader_backend_cls
from .sorter import HierarchySorter
from .stages import RequiredKeysFilter, TypeChecker
from .writer import WriterBackend, get_writer_backend_cls


@click.command()
@click.argument("file_source")
@click.option(
    "-k",
    "--keys",
    "header_string",
    required=True,
    help="Keys spec e.g. 'id:int,name:str,type:str'",
)
@click.option(
    "-h",
    "--hierarchy",
    "hierarchy_string",
    required=True,
    help="Output hierarchy specification. Example: A -> B -> C",
)
@click.option(
    "-r",
    "--reader-backend",
    type=click.Choice(ReaderBackend.choices()),
    default=ReaderBackend.LOCAL,
    help=(
        f"Force a specific reader backend. "
        f"Default: {ReaderBackend.LOCAL.name}"
    ),
)
@click.option(
    "-w",
    "--writer-backend",
    type=click.Choice(WriterBackend.choices()),
    default=WriterBackend.STDOUT,
    help=(
        f"Force a specific writer backend. "
        f"Default: {WriterBackend.STDOUT.name}"
    ),
)
def main(
    file_source: str,
    header_string: str,
    hierarchy_string: str,
    reader_backend: str | None,
    writer_backend: str | None,
):
    """
    Read a key=value CSV file and output filtered, typed rows, sorted by a
    specified hierarchy.
    """
    # Initialize various components based on the CLI args
    reader = get_reader_backend_cls(reader_backend)(file_source)
    hierarchy = Hierarchy.from_string(hierarchy_string)
    sorter = HierarchySorter(hierarchy)
    header = Header.from_string(header_string)
    writer = get_writer_backend_cls(writer_backend)(header.to_keys())

    # Parse the  data into rows of dict
    parsed_rows = IngestionParser(reader).parse()

    # Create a processing pipeline with the required stages and run it
    # on the parsed rows
    pipeline = IngestionPipeline(
        rows=parsed_rows,
        stages=[
            RequiredKeysFilter(header),
            TypeChecker(header),
        ],
    )
    processed_rows = pipeline.process()

    # Sort the processed rows according to the specified
    # hierarchy and write the output
    sorted_rows = sorter.sort(processed_rows)

    # Finally, write the sorted rows using the specified writer backend
    writer.write(rows=sorted_rows)


if __name__ == "__main__":
    main()
