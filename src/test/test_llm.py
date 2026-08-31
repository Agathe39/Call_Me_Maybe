# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_llm.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 11:16:01 by agathe          #+#    #+#               #
#  Updated: 2026/08/31 13:38:41 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from llm_sdk import Small_LLM_Model


class TestLlm:

    def __init__(self, llm: Small_LLM_Model, functions_names: dict[str, list[str]]):
        self.llm = llm
        self.functions_names = functions_names

    def generate_test(self) -> None:

        print(self.functions_names)

        prompt = "{'system': 'get parameters values in content', 'content': 'prompt', 'parameters': 'number'}\nassistant': "

    def construct_prompt(functions_names: dict[str, list[str]]): 






















    #     prompt = "{'system': 'Convert number into string number like '100' = 'hundred', nothing else.', 'content': '10'}\nassistant: "

    #     while True:

    #         encode_prompt = self.llm.encode(prompt)[0].tolist()
    #         results = self.llm.get_logits_from_input_ids(encode_prompt)
            
    #         max_token = results.index(max(results))
    #         token = self.llm.decode(max_token)

    #         if token == "\n":
    #             break

    #         prompt += token
    #         print(prompt)
    #         # print(token)
    #         print()
            