# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parameters.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/17 14:06:24 by agathe          #+#    #+#               #
#  Updated: 2026/08/24 14:34:51 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
import json


class Parameters:

    def __init__(self, functions_names: dict[str, list[str]]):
        self.functions_names = functions_names
        self.test = Small_LLM_Model()
        self.all_info: dict[str, list[str | dict[str, str]]] = {}
        self.prompts: list[list[str]] = []
        self.basics_prompts: list[list[str]] = []
        self.prompt_funct_param: dict[str, list[str]] = {}

    def parameters_calling(self) -> dict[str, list[str]]:

        self.search_info_function(self.functions_names)
        self.construct_prompts()
        self.calling_llm()

        return self.functions_names

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
                if funct_name[0] == funct:
                    self.all_info[prompt] = [funct, parameter]
                    self.prompt_funct_param[prompt] = [funct]

    def construct_prompts(self) -> None:

        for prompt, infos in self.all_info.items():

            all_param: list[str] = []
            params = infos[1][1:]
            all_param = []
            
            for param in params:

                for value in param.values():
                    p = value.get("type")
                    all_param.append(p)

            self.prompts.append(f"Function: {infos[0]} -> {infos[1][0]}\nParameters needed: {all_param}\nPrompt: {prompt}\nExtract the parameter values ->")
            self.basics_prompts.append(prompt)

    def calling_llm(self) -> None:

        voc = self.test.get_path_to_vocab_file()
        with open(voc, "r") as v:
            vocabulaire = json.load(v)

        for prompt in self.prompts:

            param_wanted = self.get_param_type(prompt)

            for nbr, param in enumerate(param_wanted):

                if param == "number":

                    very_best_token: dict[int, float] = {}
                    token_valid: list[int] = self.search_token_valid(param, vocabulaire)
                    prompt += f" parameters {nbr+1}: "

                    while ((very_best_token == {}) or (next(key for key in very_best_token) in token_valid)):

                        very_best_token = {}
                        score_valid: dict[int, float] = {}

                        tensor_prompt = self.test.encode(prompt)
                        encode_prompt = tensor_prompt[0].tolist()
                        score_prompt = self.test.get_logits_from_input_ids(encode_prompt)

                        for i, score in enumerate(score_prompt):
                            if i in token_valid:
                                score_valid[i] = score

                        if score_valid:

                            max_score_total = max([value for value in score_prompt])
                            for i, score in enumerate(score_prompt):
                                if score == max_score_total:
                                    very_best_token[i] = score

                            max_score_valid = max([value for value in score_valid.values()])

                            if max_score_total in [value for value in score_valid.values()]:
                                for key, value in score_valid.items():
                                    if value == max_score_valid:
                                        response = self.test.decode(key)
                                        prompt += f"{response}"

                    if nbr + 1 != len(param_wanted):
                        prompt += ","

                elif param == "string":

                    token: str = ""
                    prompt += f" parameters {nbr+1}: '"

                    while "'" not in token:
                    
                        encode_prompt = self.test.encode(prompt)[0].tolist()
                        all_score = self.test.get_logits_from_input_ids(encode_prompt)
                        best_score = max(value for value in all_score)
                        best_token = all_score.index(best_score)
                        token = self.test.decode(best_token)
                        prompt += token

                if nbr + 1 == len(param_wanted):
                    self.extract_param(prompt)

    def get_param_type(self, prompt: str) -> list[str]:

        cut1 = prompt.split("Parameters needed: ")[1]
        cut2 = cut1.split("\n")[0]
        cut3 = cut2.strip("[]")
        param_list = cut3.replace("'", "").split(", ")

        return param_list    

    def count_param(self, prompt: str) -> int:

        cut1: list[str] = prompt.split("[")
        cut2 = cut1[1].split("]")
        params = cut2[0].split(", ")
        lenght = len(params)

        return lenght

    def search_token_valid(self, param: str, vocabulaire: dict[str, float]) -> list[int]:

        token_valid: list[int] = []
        if param == "number":
            for key, value in vocabulaire.items():
                try:
                    if "Ġ" in key:
                        temp = key.replace("Ġ", "")
                        if "." in temp:
                            temp = temp.replace(".", "")
                        if "-" in temp:
                            temp = temp.replace("-", "")
                        float(temp)
                        token_valid.append(value)
                        continue
                    if "." in key and len(key) == 1:
                        token_valid.append(value)
                        continue
                    if "-"in key and len(key) == 1:
                        token_valid.append(value)
                        continue
                    float(key)
                    token_valid.append(value)
                except ValueError:
                    continue

        if param == "string":
            pass

        return token_valid

    def extract_param(self, prompts: str) -> None:

        prompt1 = prompts.split("Prompt: ")[1]
        prompt2 = prompt1.split("Extract")[0]

        parameters = prompts.split("values -> ")[1]

        for p in self.functions_names:
            if p in prompt2:
                self.functions_names[p].append(parameters)