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
1. Clone the repository: `git clone git@github.com:collate-hiring/jerinpetergeorge.git`
2. cd into the project directory: `cd jerinpetergeorge`
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
___
___
___

The Ingestion Game consists of:
1. A data file with a varying number of entries containing some data. It is shaped as a CSV where each row has
    an arbitrary number of `key=value` pairs separated by comma.
    ```
    key1=value1,key2=value2
    key3=value3
    key4=value4,key5=value5,key6=value6
    ```
2. Not all `key`s are always important! Each time we play the game, the keys to process can be different. The rest
    are just considered noise. We want to ingest all the important keys.
3. All important keys are always going to be present in the data rows of the input file.
4. Each `key` supports a specific data type. We should only process rows where the values match the expected datatype of each key.
5. Each row consists of an Entity of a given type. The type will be informed as `type=T` in the data. `type` is
    always considered as an important key and we can assume it is a `str`.
6. Entities have hierarchies defined in the games' rules. For example, given the rule `A -> B`, we cannot
    process any Entity of type `B` until we have processed all Entities of type `A`.

Your task is to win the Ingestion Game with the following rules:

- The important keys are `id:int`, `name:str`, `food:str` and `type:str`.
- Entities follow the hierarchy `A -> B -> C`.

The solution must be coded in Python and you can use any public libraries. The solution must be a Python package that we can execute as a CLI that outputs
the processed data to `stdout` in CSV format following the important keys, e.g.,:

```
id,name,food,type
1,levy,veggies,A
2,lima,pizza,A
3,john,fish,B
```

We are going to provide a data file with the keys and hierarchies mentioned above, but your CLI should accept any
important keys and hierarchies as inputs. You can see an example on input data in the provided `input.txt`.

## 🤓 We value in the solution

- Good software design
- Proper documentation
- Compliance to Python standards and modern usages (e.g.: [PEP8](https://peps.python.org/pep-0008/))
- Proper use of data structures
- Ergonomy of the command line interface
- Setup/Launch instructions if required

# Architecture Review

The second exercise is creating a sample architecture for your proposed solution. Instead of considering the package as a CLI, let's suppose you are now developing an "Ingestion Game" SaaS where users can upload their input data, specify the hierarchy and important keys, and expect to get the results back.

For this exercise, prepare one slide explaining the solution design in the cloud of your choice. We value topics such as scalability, reliability, portability, etc.
