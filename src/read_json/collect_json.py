# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collect_json.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 13:41:58 by agathe          #+#    #+#               #
#  Updated: 2026/08/31 14:15:31 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import json
from src.read_json.input_prompts import InputPrompts
from src.read_json.input_functions import InputFunctions

class CollectJson():

    def __init__(self):
        pass

    def collect_input_functions(self, path: str) -> InputFunctions:

        try:

            with open(path, "r") as f:
                docs = json.load(f)
                functions = InputFunctions(docs)

                return functions

        except FileNotFoundError:
            print("\nERROR: function calling file not found\n")
            sys.exit()
        except PermissionError:
            print("\nERROR: function calling file denied permission\n")
            sys.exit()

    def collect_input_prompts(self, path: str) -> InputPrompts:
        pass