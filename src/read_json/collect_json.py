# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collect_json.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 13:41:58 by agathe          #+#    #+#               #
#  Updated: 2026/08/31 17:44:37 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import json
from typing import Any
from xml.dom import ValidationErr
from src.read_json.input_functions import InputFunctions
from src.read_json.input_prompts import InputPrompts

class CollectJson:

    def collect_data(self, functions_path: str, prompts_path: str) -> dict[str, list[dict[str, Any]]]:

       functions = self.verif_input_function(functions_path)
       prompts = self.verif_input_prompts(prompts_path)

       return {"functions": functions.functions, "prompts": prompts.prompts}

    def verif_input_function(self, functions_path: str) -> InputFunctions:
        try:
        
            with open(functions_path, "r") as f:
                func = json.load(f)
                functions = InputFunctions(path=functions_path, functions=func)

                print("In functions, everythings ok")
                print()

                return functions

        except ValidationErr as e:
            print(e)
        except FileNotFoundError:
            print("\nERROR: function calling file not found\n")
            sys.exit()
        except PermissionError:
            print("\nERROR: function calling file denied permission\n")
            sys.exit()

    def verif_input_prompts(self, prompts_path: str) -> InputPrompts:

        try:
                
            with open(prompts_path, "r") as f:
                prompt = json.load(f)
                prompts = InputPrompts(path=prompts_path, prompts=prompt)

                print("In prompts, everythings ok")
                print()

                return prompts

        except ValidationErr as e:
            print(e)
        except FileNotFoundError:
            print("\nERROR: function calling file not found\n")
            sys.exit()
        except PermissionError:
            print("\nERROR: function calling file denied permission\n")
            sys.exit()
