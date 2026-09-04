# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parameters.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/17 14:06:24 by agathe          #+#    #+#               #
#  Updated: 2026/09/04 10:15:57 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from multiprocessing.util import info
import re
from llm_sdk import Small_LLM_Model
# import json
from typing import Any
# import sys


class Parameters:

    def __init__(self, llm: Small_LLM_Model, functions_names: dict[str, list[str]], json_data: dict[str, list[dict[str, Any]]]):

        self.llm = llm
        self.functions_names = functions_names
        self.json_data = json_data
        self.prompts: list[tuple[str]] = []
        self.finals_prompts: list[str] = []
        self.result: list[dict[str, str]] = []

    def parameters_calling(self) -> list[str]:
        """For each prompt, find the parameters corresponding
           to the extracted function

        Returns:
            dict[str, list[str]]: dictionnary with prompt for key
                                  and a list with the corresponding
                                  function and his parameters
        """

        self.search_info_function(self.functions_names)
        self.construct_prompts()
        self.calling_llm()
        self.organize_data()

        return self.result

    def search_info_function(self,
                             prompts_functions: dict[str, list[str]]) -> None:
        """Picks the name and the description of each functions

        Args:
            prompts_functions (dict[str, str]): dictionnary with prompt
                                                for key and function name
                                                for value
        """

        functions = self.json_data.get("functions")

        for func_info in self.functions_names.values():

            for name in func_info:

                for function in functions:
                    if function.get("name") == name:
                        
                        func_info.append(function.get("description"))
                        parameters = function.get("parameters")

                        params: list[str] = []
                        for param, type in parameters.items():
                            params.append(f"{param} ({type.get('type')})") 

                        func_info.append(params)

    def construct_prompts(self) -> None:
        """Construct a formatted prompt that the LLM can understand
        """

        system_prompt = "Give the parameters with correct type, in a content given, only that."

        self.prompts = []
        for prompt, func_info in self.functions_names.items():
            formatted = (
                "["
                "{"f"\"system\": \"{system_prompt}\"""},"
                "{"f"\"content\": \"{prompt}\"""},"
                "{"f"\"function\": \"{func_info[1]}\"""},"
                "{"f"\"parameters\": {[f.replace(' ', ':') for f in func_info[2]]}""}"
                "]\nassistant:")
            self.prompts.append((prompt, formatted))

    def calling_llm(self) -> None:
        """Give the formatted prompt to the LLM in order to extract the function's parameters.
        """

        for original_prompt, formatted_prompt in self.prompts:

            parameters = self.functions_names[original_prompt][2]

            for param in parameters:

                if "string" in param:
                    formatted_prompt += "\n" + param + ": \""
                else:
                    formatted_prompt += "\n" + param + ": "

                while True:

                    encode_prompt = self.llm.encode(formatted_prompt)[0].tolist()
                    results = self.llm.get_logits_from_input_ids(encode_prompt)

                    max_token = results.index(max(results))
                    token = self.llm.decode(max_token)

                    if "\n" in token:
                        token = token.replace("\n", "")
                        formatted_prompt += token
                        break

                    formatted_prompt += token
            
            self.finals_prompts.append(formatted_prompt)

        # for prompt in self.finals_prompts:
        #     print()
        #     print(prompt)
        #     print()
        #     print("---------------------------------------------------------------")

    def organize_data(self) -> None:
        """Organize data in order to send it to the construct json class
        """

        for prompt, funct_info in self.functions_names.items():
            for i in range(len(self.finals_prompts)):
                if prompt in self.finals_prompts[i]:
                    self.finals_prompts[i] += f"\nfunction_name: {funct_info[0]}"

        self.create_dictionnary()

    def create_dictionnary(self) -> None:
        """Create a dictionnary with the data
        """

        prompt: str = ""
        name: str = ""
        parameters: dict[str, str] = {}

        for formatted_prompt in self.finals_prompts:

            cut1 = formatted_prompt.split(': ')

            prompt = cut1[2].replace('},{"function"', "")
            name = cut1[-1]

            cut1_parameters = formatted_prompt.split("assistant")[1]
            cut2_parameters = cut1_parameters.split("\n")
            cut3_parameters = [param.split(": ") for param in cut2_parameters]
            cut4_parameters = cut3_parameters[1:-1]
            cut5_parameters = [param[-1] for param in cut4_parameters]

            functions = self.json_data.get("functions")
            for function in functions:
                parameters = {}
                if function.get("name") == name:
                    for i, parameter in enumerate(function.get("parameters")):
                        try:
                            value = cut5_parameters[i]
                            value = float(value)
                            parameters[parameter] = value
                        except ValueError:
                            value = value.strip('"')
                            parameters[parameter] = value

                    self.result.append({"prompt": prompt, "name": name, "parameters": parameters})
