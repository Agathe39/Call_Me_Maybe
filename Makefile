.SILENT:

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
			 --ignore-missing-imports \
			 --disallow-untyped-defs \
			 

.PHONY: all run install debug lint lint-strict clean fclean help


all: install run

run:
	uv run python -m src

install: 
	uv sync
	uv add pydantic flake8 mypy pytest numpy

debug:
	python -m pdb src

lint:
	uv run python -m flake8 .
	uv run python -m mypy . $(MYPY_FLAGS)

lint-strict:
	uv run python -m flake8 .
	uv run python -m mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} \;
	rm -rf .mypy_cache
	rm -rf .pytest_cache

fclean:
	rm -rf .venv

help:
	echo "make install: generates the virtual environment and installs the dependencies"
	echo "make run: run the programe"
	echo "make debug: launches the Pdb debugging tool"
	echo "make lint: run flake8 and mypy"
	echo "make lint-strict: run flake8 and mypy more strictly"
	echo "make clean: delete the cache"
	echo "make fclean: delete the virtual environnement"

