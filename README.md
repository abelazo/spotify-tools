# Spotify tools

| Configuration                                                                                                                                                                                                   | Status                                                                                                                                  |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| [![Semantic Release](https://github.com/abelazo/spotify-tools/actions/workflows/semantic-release.yaml/badge.svg?branch=main)](https://github.com/abelazo/spotify-tools/actions/workflows/semantic-release.yaml) | [![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) |
| [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)                                                    | [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)                                    |

Tools to interact with Spotify API

## Getting started

### Prerequisites

- [ ] TBC

### Installation

#### Prepare local environment

Install pre-commits for this repo and python dependencies:

```shell
just setup
```

## Usage

Run the API using Just:

```shell
just run
```

## Contributing

### Run tests

You can simply use just to run the tests

```shell
just test    # Runs a subset of tests
just testall # Runs all tests
```

You can also use pytest directly:

```shell
poetry run pytest                        # Runs all tests
poetry run pytest -m "marks expression"  # Runs tests with a specific mark
poetry run pytest test/                  # Runs tests in test/ folder
poetry run pytest test_mod.py::test_func # Runs specific test within a module
```

## License

Distributed under the GPL 3.0 License. See [LICENSE.txt](LICENSE.txt) for more information.

## Support

You can contact [me](https://github.com/abelazo).
