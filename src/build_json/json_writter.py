# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  json_writter.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/26 13:39:42 by agathe          #+#    #+#               #
#  Updated: 2026/08/27 14:05:57 by agathe          ###   ########.fr        #
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

        try:
            with open(sys.argv[3], "w") as write:
                data = [{"hello": "world", "bonjour": "tout le monde"}]
                json.dump(data, write, indent=4)
        except FileNotFoundError:
            print("ERROR: function calling results file not found")
            sys.exit()
        except PermissionError:
            print("ERROR: function calling results file denied permission")
            sys.exit()

    def get_func(self) -> list[dict]:

        try:
            with open(sys.argv[1], "r") as file:
                docs = json.load(file)
                # print("docs:", docs)
                # print()
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

        print("param:", param)
        print("name_param", name_param)
        print()
        
        self.data.append({"prompt": prompt, "name": name, "parameters": {}})

    def purge_param(self, parameters: list[str]) -> list[str]:

        all_param: list[str] = []
        for i, param in enumerate(parameters):
            all_param.append(param.strip(f"parameters {i+1}: "))

        return all_param