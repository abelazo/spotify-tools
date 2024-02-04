set dotenv-load

# Print just help
default:
	@just --list

# Setup the local environment
setup:
	poetry install
	poetry run pre-commit install -t commit-msg -t pre-commit -t pre-merge-commit

# Run specific tests subset
test target="ut":
    poetry run pytest -m {{target}}

# Run all tests
test-all: (test "ut")

# Run black and ruff
lint:
	poetry run black . && poetry run ruff --fix .

run:
    poetry run importer
