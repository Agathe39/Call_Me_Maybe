# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parameters.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/17 14:06:24 by agathe          #+#    #+#               #
#  Updated: 2026/08/18 17:06:22 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
import json


class Parameters:

    def __init__(self):
        self.test = Small_LLM_Model()
        self.all_info: dict[str, list[str | dict[str, str]]] = {}
        self.prompts: list[list[str]] = []
        self.basics_prompts: list[list[str]] = []
        self.prompt_funct_param: dict[str, list[str]] = {}

    def parameters_calling(self, prompts_functions: dict[str, str]) -> dict[str, list[str]]:

        self.search_info_function(prompts_functions)
        self.construct_prompts()
        self.calling_llm()
        

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

            self.prompts.append(f"Function: {infos[0]} -> {infos[1][0]}\nParameters needed: {all_param}\nPrompt: {prompt}\nExtract the parameter values ")
            self.basics_prompts.append(prompt)
            
        for prom in self.prompts:
            print(prom)
            print()

    def calling_llm(self) -> None:

        for prompt in self.basics_prompts:

            print(prompt)
            token_prompt = self.test.encode(prompt)[0].tolist()
            score_next_token = self.test.get_logits_from_input_ids(token_prompt)

            score: list[float] = []
            for token in token_prompt:
                try:
                    score.append(score_next_token[token])
                except ValueError:
                    pass

            max_score = max(score)
            max_token = next(token_prompt[i] for i, s in enumerate(score) if s == max_score)
            print(self.test.decode(max_token))
                












        # search_param: list[str] = []
        # for i, final_prompt in enumerate(self.prompts):

            # search_param = []
            # nbr_param = self.count_param(final_prompt)

            # while len(search_param) < nbr_param:

            # print(final_prompt)

            # tensor_p_final = self.test.encode(final_prompt)
            # token_p_final = tensor_p_final[0].tolist()

            # tensor_p = self.test.encode(self.basics_prompts[i])
            # token_p = tensor_p[0].tolist()
            # print(token_p_final)
            # print(token_p)
            # print()

            # all_final_tokens = self.test.get_logits_from_input_ids(token_p_final)

            # final_token: list[float] = []
            # for token in token_p:
            #     final_token.append(all_final_tokens[token])

            # print(token_p)
            # print(final_token)
            # max_score = max(final_token)
            # print(max_score)
            # best_token = final_token.index(max_score)
            # print(self.test.decode(best_token))
            # try:
            #     print(self.test.decode(token_p[12]))
            # except IndexError:
            #     pass
                

    def count_param(self, prompt: str) -> int:

        cut1: list[str] = prompt.split("[")
        cut2 = cut1[1].split("]")
        params = cut2[0].split(", ")
        lenght = len(params)

        return lenght