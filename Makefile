.SILENT:

FUNC_DEF = "data/input/functions_definition.json"
INPUT_FILE = "data/input/function_calling_tests.json"
OUTPUT_FILE = "data/output/function_calling_results.json"
MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
			 --ignore-missing-imports \
			 --disallow-untyped-defs \
			 --check-untyped-defs

include .env


.PHONY: all run install debug lint lint-strict clean fclean help


all: install run

run:
	uv run python -m src --functions_definition $(FUNC_DEF) --input $(INPUT_FILE) --output $(OUTPUT_FILE)

install:
	uv sync
	uv add pydantic flake8 mypy pytest numpy torch transformers huggingface-hub

debug:
	python -m pdb -m src

lint:
	uv run python -m flake8 .
	uv run python -m mypy . $(MYPY_FLAGS)

lint-strict:
	uv run python -m flake8 .
	uv run python -m mypy . --strict

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(OUTPUT_FILE)
	rm -rf "data/output"

fclean: clean
	rm -rf .cache
	rm -rf .llm
	rm -rf .venv

help:
	echo "\n"
	echo "make install: generates the virtual environment and installs the dependencies"
	echo "make run: run the programe"
	echo "make debug: launches the Pdb debugging tool"
	echo "make lint: run flake8 and mypy"
	echo "make lint-strict: run flake8 and mypy more strictly"
	echo "make clean: delete the cache"
	echo "make fclean: delete the virtual environnement"
	echo "\n"

