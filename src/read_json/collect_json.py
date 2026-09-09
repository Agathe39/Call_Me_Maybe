# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collect_json.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 13:41:58 by agathe          #+#    #+#               #
#  Updated: 2026/09/09 18:19:37 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import json
from json import JSONDecodeError
from typing import Any
from pydantic import BaseModel, ValidationError
from src.read_json.input_functions import InputFunctions
from src.read_json.input_prompts import InputPrompts


class CollectJson(BaseModel):
    """Loads and validates functions and prompts from JSON files.

    Uses the corresponding Pydantic models to verify that the content
    of the input JSON files has the expected structure.
    """

    def collect_data(self, functions_path: str,
                     prompts_path: str) -> dict[str, list[dict[str, Any]]]:
        """Collect functions and prompts in JSON files

        Args:
            functions_path (str): path to JSON functions path
            prompts_path (str): path to JSON prompts path

        Returns:
            dict[str, list[dict[str, Any]]]: dict with functions and prompts
        """

        functions = self.verif_input_function(functions_path)
        prompts = self.verif_input_prompts(prompts_path)

        return {"functions": functions.functions, "prompts": prompts.prompts}

    def verif_input_function(self, functions_path: str) -> InputFunctions:
        """Open and verify the JSON function is valid

        Args:
            functions_path (str): path to JSON functions file

        Returns:
            InputFunctions: pydantic class valid of JSON functions file
        """
        try:

            with open(functions_path, "r") as f:
                func = json.load(f)
                functions = InputFunctions(path=functions_path, functions=func)

                print("\nFunctions calling file is verified, everythings ok")
                print()

                return functions

        except FileNotFoundError:
            print("\nERROR: function calling file not found\n")
            sys.exit()
        except PermissionError:
            print("\nERROR: function calling file denied permission\n")
            sys.exit()
        except JSONDecodeError:
            print("\nERROR: Json syntax of function calling file is false\n")
            sys.exit()
        except UnicodeDecodeError:
            print("\nERROR: function calling file is not a text document")
            sys.exit()
        except ValidationError as exc:
            print("\n", repr(exc.errors()[0]['msg']))
            print()
            sys.exit()

    def verif_input_prompts(self, prompts_path: str) -> InputPrompts:
        """Open and verify the JSON prompts is valid

        Args:
            prompts_path (str): path to JSON prompts file

        Returns:
            InputPrompts: pydantic class valid of JSON prompts file
        """

        try:

            with open(prompts_path, "r") as f:
                prompt = json.load(f)
                prompts = InputPrompts(path=prompts_path, prompts=prompt)

                print("Prompts calling file is verified, everythings ok")
                print()

                return prompts

        except FileNotFoundError:
            print("\nERROR: prompt calling file not found\n")
            sys.exit()
        except PermissionError:
            print("\nERROR: prompt calling file denied permission\n")
            sys.exit()
        except json.JSONDecodeError:
            print("\nERROR: Json syntax of prompt calling file is false\n")
            sys.exit()
        except UnicodeDecodeError:
            print("\nERROR: prompt calling file is not a text document\n")
            sys.exit()
        except ValidationError as exc:
            print(repr(exc.errors()[0]['msg']))
            print()
            sys.exit()
