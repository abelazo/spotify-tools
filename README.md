# Spotify tools
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
