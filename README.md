*This project has been created as part of the 42 curriculum by aeuvrard.*

# Call Me Maybe

## Description

Call Me Maybe is a function calling tool that translates natural language prompts into structured, machine executable function calls. Given a prompt such as "What is the sum of 40 and 2?", the program does not answer the question directly. Instead, it identifies which function should be called and with which arguments, and produces a strict JSON output such as:

```json
{
  "prompt": "What is the sum of 40 and 2?",
  "name": "fn_add_numbers",
  "parameters": {"a": 40.0, "b": 2.0}
}
```

The project relies on a small local language model (Qwen/Qwen3-0.6B, 500 million parameters) accessed through the provided `llm_sdk` wrapper. Rather than hoping the model spontaneously produces valid JSON, the program constrains the model's token generation so that the selected function name is always one of the functions declared in `functions_definition.json`, and so that every produced result is syntactically valid JSON.

## Instructions

### Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) as the package manager

### Installation

```bash
make install
```

This runs `uv sync` and installs the project dependencies (pydantic, flake8, mypy, pytest, numpy) together with the dependencies required by `llm_sdk` (torch, transformers, huggingface-hub) so that the reviewer only ever needs a single `uv sync` at the repository root.

### Running the program

```bash
uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--output <output_file>]
```

All three flags are optional. When omitted, the program falls back to the default locations expected by the subject:

| Flag                     | Default value                                  |
|---------------------------|-------------------------------------------------|
| `--functions_definition`  | `data/input/functions_definition.json`           |
| `--input`                 | `data/input/function_calling_tests.json`         |
| `--output`                | `data/output/function_calling_results.json`      |

Example with explicit paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

Equivalently, through the Makefile:

```bash
make run
```

### Other Makefile targets

- `make debug` runs the program under Python's built-in debugger (`pdb`).
- `make lint` runs `flake8` and `mypy` with the flags required by the subject.
- `make lint-strict` runs `flake8` and `mypy --strict`.
- `make clean` removes `__pycache__`, `.mypy_cache`, `.pytest_cache` and the generated output file.
- `make fclean` removes the virtual environment.

The `data/output/` directory is not versioned (see `.gitignore`), since the subject asks for it not to be included in the submission. The program creates it automatically on first run if it does not already exist, so no manual step is required after cloning the repository.

## Algorithm explanation

The pipeline is split into two constrained decoding stages, handled by two different classes.

### Stage 1: function name selection (`FunctionCalling`)

1. Every function name declared in `functions_definition.json` is tokenized in advance, producing one list of token ids per function.
2. A prompt is built, listing every available function with its description, followed by the user's prompt.
3. At each generation step, the model produces logits for the next token from the current context.
4. Instead of picking the single highest scoring token over the entire vocabulary, the candidate function names are first filtered down to only those whose token sequence still matches every token generated so far (a prefix check, similar to walking a trie of the allowed function names).
5. Among the tokens that keep at least one candidate valid, the token with the highest logit is selected. Tokens that would break every remaining candidate are effectively excluded from consideration.
6. As soon as a single candidate remains, its remaining tokens are appended directly and generation for the function name stops.

This guarantees that the function name returned by the program is always exactly one of the names declared in `functions_definition.json`, since no other token sequence can ever survive the filtering step.

### Stage 2: parameter extraction (`Parameters`)

1. For the function selected in stage 1, a second prompt is built from its description and the type of each of its parameters (as declared in `functions_definition.json`).
2. For each parameter, the prompt is extended with its name and expected type, then the model generates tokens greedily (highest logit at every step) until it produces a token containing a newline character, which marks the end of that parameter's value.
3. Once every parameter has been generated as raw text, each value is parsed: if it can be converted with `float(...)`, it is stored as a number, otherwise it is kept as a string (surrounding quotes are stripped).

The final JSON file is produced with Python's built-in `json` module, which by construction only ever writes syntactically valid JSON: since every parameter value is, at that point, a native Python `float` or `str`, there is no possibility of malformed JSON reaching the output file.

## Design decisions

- **Two different strategies for two different problems.** The set of valid function names is small, fixed, and fully known in advance, which makes it a very good fit for the trie based, token level filtering described above: it is cheap to enumerate every allowed continuation. Parameter values, on the other hand, are open ended (any number, any string), so the same trie approach does not apply directly; the program instead relies on a structured prompt template plus a final type cast to guarantee that the values that reach the JSON writer are always well typed.
- **Pydantic for every custom class.** All data-holding classes in `src/` (`InputFunctions`, `InputPrompts`, `CollectJson`, `FunctionCalling`, `Parameters`, `JsonWritten`) are pydantic `BaseModel` subclasses, as required by the subject. Command line argument parsing, on the other hand, is handled by the standard `argparse` module through a plain function rather than a class, since it is not a data-holding object that needs validation.
- **A single `pyproject.toml` at the repository root.** `llm_sdk` is a package provided as part of the subject rather than code written for this project, so its own dependencies (`torch`, `transformers`, `huggingface-hub`) are declared alongside the project's own dependencies (`pydantic`, `numpy`) in the same `pyproject.toml`. This matches the subject's expectation that the reviewer only ever runs `uv sync` once, at the root of the repository.
- **Graceful error handling everywhere a file is touched.** Every place that opens or parses a JSON file (`CollectJson`) or writes one (`JsonWritten`) is wrapped in `try/except`, with a clear, user facing error message for missing files, permission errors, and invalid JSON syntax, instead of letting the program crash with a raw traceback.

## Performance and reliability

- **Function name selection** is deterministic and, by construction, always returns one of the declared function names: it cannot fail to produce valid JSON at that stage, regardless of the size or wording of the user prompt.
- **JSON validity** of the final output file is guaranteed independently of the model's behaviour, since the output is always built from native Python types and serialized with the standard `json` module.
- **Argument extraction accuracy** (whether the extracted numbers and strings match the intent of the prompt) depends on the quality of the underlying 0.6B model's greedy decoding and is the part most likely to need manual review on ambiguous or unusual prompts.
- Measured accuracy, throughput, and wall clock time on the sample files in `data/input/` should be recorded here once you run your own benchmark, for example: number of prompts processed, total processing time, and the proportion of prompts for which the extracted arguments matched the expected values by inspection.

## Challenges faced

- **Reconciling `argparse` with the pydantic-based architecture.** The subject requires every class to use pydantic, but command line argument parsing does not need to be a class at all; the solution was to keep `argparse` as a plain function that feeds already-validated data into the existing pydantic models, rather than forcing an unnecessary class around it.
- **The `data/output/` directory is intentionally excluded from the repository**, which means it does not exist right after a fresh clone. The program creates it on demand (`os.makedirs(..., exist_ok=True)`) before writing the result file, so the very first run after cloning does not fail with a missing directory error.
- **A race condition in the `clean` Makefile target.** The original `find . -type d -name "__pycache__" -exec rm -rf {} \;` command could return a non-zero exit status if `find` tried to descend into a directory that had just been deleted by an earlier `-exec` call in the same pass, which silently stopped the rest of the `clean` rule on the first run. Adding `-prune` to stop `find` from recursing into a match it is about to delete resolved the issue.

## Testing strategy

- The program was run manually against the sample files provided in `data/input/` (`functions_definition.json` and `function_calling_tests.json`), covering functions with numeric parameters, string parameters, and no parameters.
- The resulting `data/output/function_calling_results.json` file was checked for JSON validity (it parses without error) and for schema compliance (every object has exactly the keys `prompt`, `name`, `parameters`, and the parameter types match the corresponding function's declaration).
- Error handling was tested by pointing `--functions_definition` and `--input` at missing files and at files containing deliberately malformed JSON, confirming that the program prints a clear error message and exits instead of crashing.
- The subject recommends, but does not require for grading, an automated `pytest` or `unittest` suite for local development; none is included in the submission, in line with the subject's instructions.

## Example usage

Using the default paths:

```bash
make install
make run
```

Using explicit paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

Sample input (`data/input/function_calling_tests.json`):

```json
[
  { "prompt": "What is the sum of 2 and 3?" },
  { "prompt": "Reverse the string 'hello'" }
]
```

Corresponding output (`data/output/function_calling_results.json`):

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {"a": 2.0, "b": 3.0}
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {"s": "hello"}
  }
]
```

## Resources

- [Python `argparse` documentation](https://docs.python.org/3/library/argparse.html)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [uv documentation](https://docs.astral.sh/uv/)
- [JSON specification](https://www.json.org/)
- [Qwen3 model card on Hugging Face](https://huggingface.co/Qwen/Qwen3-0.6B)
- General background reading on constrained / grammar-guided decoding of language models

### How AI was used

Claude (Anthropic) was used as a learning aid throughout this project, in the following ways:

- Explaining, with a generic example unrelated to this project's code, how Python's `argparse` module works (`ArgumentParser`, `add_argument`, `parse_args`), before the corresponding flags were written by hand for this project.
- Clarifying the separation of concerns between command line argument parsing and the existing pydantic models (`InputFunctions`, `InputPrompts`), and why the former does not need to be wrapped in a class to satisfy the subject's pydantic requirement.
- Explaining why the output file could not be created right after a fresh clone (`data/output/` being absent from the repository) and how `os.makedirs(..., exist_ok=True)` solves it.
- Helping draft this README file itself, based on a description of the project's actual source code and the subject's requirements.

All code in `src/` was written and typed by the author; AI assistance was limited to explanations, generic examples, and conceptual guidance, in line with the "good practice" examples described in the subject's AI Instructions chapter.
