# The Ingestion Game

A Python CLI tool that parses a custom key-value CSV format, filters rows by important keys and valid data types, and outputs processed entities in dependency order.

## How It Works
 
### Input Format
 
The input is a CSV-like file where each row contains an arbitrary number of `key=value` pairs:
 
```
key1=value1,key2=value2
key3=value3
key4=value4,key5=value5,key6=value6
```
 
### Rules
 
1. **Important keys:** Only a defined subset of keys are relevant; all others are treated as noise.
2. **Type validation:** Each important key has an expected data type (e.g., `int`, `str`). Rows where a value doesn't match the expected type are skipped.
3. **All important keys must be present:** Every valid data row is guaranteed to contain all important keys.
4. **Entity types:** Each row represents an entity. The `type` key (always a `str`) identifies the entity's type.
5. **Hierarchy enforcement:** Entities have a processing order. For example, given `A -> B -> C`, all `A` entities must be processed before any `B`, and all `B` before any `C`.
 
## Installation

### Pre-requisites
- Python 3.10 or higher
- virtualenv (optional but recommended)
- [uv](https://docs.astral.sh/uv/) package manager

### Steps
1. Clone the repository: `git clone git@github.com:jerinpetergeorge/data-ingestion.git`
2. cd into the project directory: `cd data-ingestion`
3. Create a virtual environment (using `uv` - see [doc](https://docs.astral.sh/uv/pip/environments/#creating-a-virtual-environment)): `uv venv` and activate it
4. Install the package using uv: `uv pip install .`
5. Run the CLI: `ingestion-game --help` to see the available options

---

## Usage

```bash
ingestion-game FILE_SOURCE -k "KEYS" -h "HIERARCHY"
```

| Argument | Short | Required | Default | Description |
|---|---|---|---|---|
| `FILE_SOURCE` | — | Yes | — | Path or URL to the input file |
| `--keys` | `-k` | Yes | — | Key spec e.g. `id:int,name:str,type:str` |
| `--hierarchy` | `-h` | Yes | — | Output hierarchy e.g. `A -> B -> C` |
| `--reader-backend` | `-r` | No | `LOCAL` | One of `LOCAL`, `URL`, `S3` |
| `--writer-backend` | `-w` | No | `STDOUT` | One of `STDOUT`, `CSV` |

### Examples

```bash
# local file
ingestion-game input.txt -k "id:int,name:str,type:str" -h "A -> B -> C"
```

**Note**: Currently, only `LOCAL` reader backend and `STDOUT` writer backend are implemented.

---

## Running Tests

```bash
uv run pytest --cov .
```

___
## Ingestion Game SaaS Architecture

1. [Presentation - Google Slides](https://docs.google.com/presentation/d/126KfGYydqD6XTD8PcXwFVmsL3gjwl6i-GiUkVT3k0KA/edit?usp=sharing)
2. [Presentation - PDF](docs/System%20Design%20-%20Ingestion%20Game%20SaaS.pdf)
3. [High-level architecture diagram - Image](docs/IG-SD-02.png)
4. [High-level architecture diagram - Excalidraw File](docs/IG-SD-01.excalidraw)
