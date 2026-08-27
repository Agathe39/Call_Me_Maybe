# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  json_writter.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/26 13:39:42 by agathe          #+#    #+#               #
#  Updated: 2026/08/27 16:45:41 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import json


class JsonWritten:

    def __init__(self) -> None:
        self.data: list[dict] = []

    def write_output(self, functions_parameters: dict[str, list[str]]) -> None:

        docs = self.get_func()

        for prompt, func_param in functions_parameters.items():
            name_param: list[str] = self.get_parameters_name(func_param[0], docs)
            self.transform_data(prompt, func_param, name_param)

        self.create_json()

    def get_func(self) -> list[dict]:

        try:

            with open(sys.argv[1], "r") as file:
                docs = json.load(file)

        except FileNotFoundError:
            print("ERROR: function calling results file not found")
            sys.exit()
        except PermissionError:
            print("ERROR: function calling results file denied permission")
            sys.exit()

        return docs

    def get_parameters_name(self, func: str, docs: list[dict]) -> list[str]:

        result: list[str] = []

        for function in docs:
            if function.get("name") == func:
                param = function.get("parameters")
                for name in param:
                    if name != "return":
                        result.append(name)

        return result

    def transform_data(self, prompt: str, func_param: list[str], name_param: list[str]) -> None:

        name: str = func_param[0]
        func_param.remove(name)

        param = self.purge_param(func_param)
        parameters = self.organise_param(param, name_param)
        
        self.data.append({"prompt": prompt, "name": name, "parameters": parameters})

    def purge_param(self, parameters: list[str]) -> list[str]:

        params = parameters[0].split(", ")

        all_param: list[str] = []

        for i, param in enumerate(params):
            if "\n" in param:
                param = param.split("\n")[0]
            param = param.replace(f"parameters {i+1}:", "")
            param = param.replace("'", "")
            param = param.replace(" ", "")
            all_param.append(param)

        return all_param

    def organise_param(self, param, name_param) -> dict[str, str | float]:

        parameters: dict[str, str | float] = {}

        for i, name in enumerate(name_param):

            try:
                param[i] = float(param[i])
            except ValueError:
                pass

            parameters[name] = param[i]

        return parameters

    def create_json(self) -> None:

        try:
        
            with open(sys.argv[3], "w") as write:
                json.dump(self.data, write, indent=4)
                print(f"\nYou can open {sys.argv[3]}, that's ready ! :)\n")

        except FileNotFoundError:
            print("ERROR: function calling results file not found")
            sys.exit()
        except PermissionError:
            print("ERROR: function calling results file denied permission")
            sys.exit()
