.SILENT:

PYTHON= python3
MAIN= src/main.py
CONFIG= maps/easy/01_linear_path.txt
MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
			 --ignore-missing-imports \
			 --disallow-untyped-defs \
			 

.PHONY: all run install debug lint lint-strict clean fclean help

all: install run

run:
	uv run $(PYTHON) $(MAIN)

install: 
	uv sync
	uv add pydantic flake8 mypy pytest torch transformers huggingface-hub numpy

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	uv run $(PYTHON) -m flake8 src/ $(MAIN)
	uv run $(PYTHON) -m mypy $(MYPY_FLAGS) $(MAIN)

lint-strict:
	uv run $(PYTHON) -m flake8 src/ $(MAIN)
	uv run $(PYTHON) -m mypy $(MYPY_FLAGS) --strict $(MAIN)

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
	echo "make run CONFIG='map path': change map"
	echo "Maps :"
	echo "	- easy :"
	echo "		maps/easy/01_linear_path.txt"
	echo "		maps/easy/02_simple_fork.txt"
	echo "		maps/easy/03_basic_capacity.txt"
	echo "	- medium :"
	echo "		maps/medium/01_dead_end_trap.txt"
	echo "		maps/medium/02_circular_loop.txt"
	echo "		maps/medium/03_priority_puzzle.txt"
	echo "	- hard :"
	echo "		maps/hard/01_maze_nightmare.txt"
	echo "		maps/hard/02_capacity_hell.txt"
	echo "		maps/hard/03_ultimate_challenge.txt"
	echo "	- challenger :"
	echo "		maps/challenger/01_the_impossible_dream.txt"