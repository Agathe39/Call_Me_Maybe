# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parameters.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/17 14:06:24 by agathe          #+#    #+#               #
#  Updated: 2026/08/17 16:12:38 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
import json


class Parameters:

    def __init__(self):
        self.test = Small_LLM_Model
        self.all_info: dict[str, list[str | dict[str, str]]] = {}
        self.prompts: list[list[str]] = []
        self.prompt_funct_param: dict[str, list[str]] = {}

    def parameters_calling(self, prompts_functions: dict[str, str]) -> dict[str, list[str]]:

        self.search_info_function(prompts_functions)
        self.construct_prompts()
        

    def search_info_function(self, prompts_functions: dict[str, str]) -> None:

        all_parameters: dict[str, list[dict, str]] = {}

        try:

            with open("data/input/functions_definition.json", "r") as f:
                docs = json.load(f)
                for doc in docs:
                    all_parameters[doc.get("name")] = [doc.get("description"), doc.get("parameters")]
 
        except FileNotFoundError:
            print("ERROR: file not found")
            return
        except PermissionError:
            print("ERROR: no permission to read the file")
            return

        for prompt, funct_name in prompts_functions.items():
            for funct, parameter in all_parameters.items():
                if funct_name == funct:
                    self.all_info[prompt] = [funct, parameter]
                    self.prompt_funct_param[prompt] = [funct]

        # print()
        # print()
        # for p, info in self.all_info.items():
        #     print(p, ":", info)
        #     print()

    def construct_prompts(self) -> None:

        print()
        print()

        for prompt, infos in self.all_info.items():

            all_param: list[str] = []
            params = infos[1][1:]
            all_param = []
            
            for param in params:

                for value in param.values():
                    p = value.get("type")
                    all_param.append(p)

            self.prompts.append(f"Function: {infos[0]} -> {infos[1][0]}\nParameters needed: {all_param}\nPrompt: {prompt}\nExtract the parameter values")
            
        for prom in self.prompts:
            print(prom)
            print()
