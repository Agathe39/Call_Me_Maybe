# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parameters.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/17 14:06:24 by agathe          #+#    #+#               #
#  Updated: 2026/09/02 17:02:04 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

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

    def parameters_calling(self) -> dict[str, list[str]]:
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

        # return self.functions_names

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

        finals_prompts: list[str] = []

        for original_prompt, formated_prompt in self.prompts:

            parameters = self.functions_names[original_prompt][2]

            for param in parameters:

                if "string" in param:
                    formated_prompt += "\n" + param + ": \""
                else:
                    formated_prompt += "\n" + param + ": "

                while True:

                    encode_prompt = self.llm.encode(formated_prompt)[0].tolist()
                    results = self.llm.get_logits_from_input_ids(encode_prompt)

                    max_token = results.index(max(results))
                    token = self.llm.decode(max_token)

                    if "\n" in token:
                        token = token.replace("\n", "")
                        formated_prompt += token
                        break

                    formated_prompt += token
            
            finals_prompts.append(formated_prompt)

        for prompt in finals_prompts:
            print()
            print(prompt)
            print()
            print("---------------------------------------------------------------")

    def search_parameters(self, prompt: str):

        parameters: list[str] = []

        cut1 = prompt.split("'prompt': ")[1]
        input_prompt = cut1.split(", \n'function':")[0]
        input_prompt = input_prompt.strip("'")

        for p, func_info in self.functions_names.items():
            if p == input_prompt:
                parameters = func_info[2]
        return parameters
