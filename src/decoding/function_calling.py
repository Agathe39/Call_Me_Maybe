# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  function_calling.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/14 13:20:52 by agathe          #+#    #+#               #
#  Updated: 2026/08/24 14:10:48 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
import json


class FunctionCalling:

    def __init__(self):

        self.test = Small_LLM_Model()
        self.functions_names: list[str] = []
        self.functions_id: list[list[int]] = []
        self.function_descriptions: list[str] = []
        self.all_functions_id: list[int] = []
        self.prompts: list[str] = []
        self.first_prompt: str = ""
        self.end_prompt: str = "Given the prompt above, "\
                               "the matching function is: "
        self.final_prompt: str = ""
        self.result: dict[str, str] = {}

    def function_response(self) -> dict[str, list[str]]:
        """Search for each prompt a compatible function name

        Returns:
            dict[str, str]: key = prompt and value = function's name
        """
        try:
            self.get_functions_info()
        except PermissionError:
            print("ERROR: denied permission")
            return
        except FileNotFoundError:
            print("ERROR: file not found")
            return

        print()

        try:
            self.get_prompts()
        except PermissionError:
            print("ERROR: denied permission")
            return
        except FileNotFoundError:
            print("ERROR: file not found")
            return

        self.construct_prompt()

        max_len = max([len(ids) for ids in self.functions_id])

        for prompt in self.prompts:

            self.final_prompt = self.first_prompt + \
                                prompt + "\n" + \
                                self.end_prompt

            self.max_tokens: list[int] = []
            self.ids_token: list[float] = []

            self.need_break: bool = False

            self.encode_prompt = self.test.encode(
                self.final_prompt).tolist()[0]

            self.ids_prompt = self.test.get_logits_from_input_ids(
                self.encode_prompt)

            self.get_valid_function(max_len)

            self.final_prompt = self.test.decode(self.encode_prompt)

            self.recup_result()

        return self.result

    def get_functions_info(self) -> None:
        """Get the name and the description for each function
        """

        with open("data/input/functions_definition.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                self.functions_names.append(doc.get("name"))
                self.function_descriptions.append(doc.get("description"))

        for name in self.functions_names:
            self.functions_id.append(self.test.encode(name).tolist()[0])
            self.all_functions_id.extend(self.test.encode(name).tolist()[0])

    def get_prompts(self) -> list:
        """Get all prompts

        Returns:
            list: all prompts
        """

        with open("data/input/function_calling_tests.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                self.prompts.append(doc.get('prompt'))

    def construct_prompt(self) -> None:
        """Construct a prompt with name and descrition functions
        """

        for i, name in enumerate(self.functions_names):
            self.first_prompt += f"Function {i}: {name} " \
                                 f"-> {self.function_descriptions[i]} \n"

    def get_valid_function(self, max_len) -> None:
        """Compare functions with prompt to keep only
           possible functions depending on prompt

        Args:
            max_len (_type_): length of the longest
                              token list for the functions
        """

        for nbr in range(max_len):

            self.functions_id_valid: list[int] = []

            ids_prompt = self.test.get_logits_from_input_ids(
                self.encode_prompt)

            self.determines_valid_function()

            if self.need_break is True:
                self.final_prompt = self.test.decode(self.encode_prompt)
                break

            ids_token = self.search_token(ids_prompt, nbr)

            self.max_score = max([score[0] for score in ids_token])
            self.max_token = next(tok[1] for tok in ids_token
                                  if tok[0] == self.max_score)
            self.max_tokens.append(self.max_token)
            self.encode_prompt.append(self.max_token)

    def search_token(self, ids_prompt, nbr) -> list[list[float | int]]:

        ids_token = []

        for tokens in self.functions_id_valid:
            try:
                ids_token.append([ids_prompt[tokens[nbr]], tokens[nbr]])
            except IndexError:
                continue

        return ids_token

    def determines_valid_function(self) -> None:
        """Compare token optained witn function's token
           to determined the valid function
        """

        for tokens in self.functions_id:
            if self.max_tokens == []:
                self.functions_id_valid.append(tokens)

            else:
                verif: bool = False
                for tok in self.max_tokens:
                    if tok in tokens:
                        verif = True
                    else:
                        verif = False
                        break
                if verif is True:
                    self.functions_id_valid.append(tokens)

        if len(self.functions_id_valid) == 1:
            for id in self.functions_id:
                if id == self.functions_id_valid[0]:
                    last_token = id.index(self.encode_prompt[-1]) + 1
                    try:
                        for token in id[last_token:]:
                            self.encode_prompt.append(token)
                    except IndexError:
                        pass
                    self.need_break = True
                    break

    def recup_result(self) -> None:
        """Matches the prompt with the expected function name
        """

        final_prompt_split: list[str] = self.final_prompt.split("\n")
        prompt_response: list[str] = final_prompt_split[-2:]

        prompt: str = prompt_response[0]
        function: str = prompt_response[-1].split(": ")[1]

        self.result[prompt] = [function]
