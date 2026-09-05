# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  function_calling.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/14 13:20:52 by agathe          #+#    #+#               #
#  Updated: 2026/09/05 19:20:25 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from pydantic import BaseModel, ConfigDict, PrivateAttr
from llm_sdk import Small_LLM_Model


class FunctionCalling(BaseModel):
    """Matches user prompts with the most appropriate function name.

    Uses the LLM to compare the tokens generated for each available
    function with the user prompt and selects the function corresponding
    to the intended action.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    llm: Small_LLM_Model
    json_data: dict[str, list[dict[str, Any]]]

    functions_names: list[str] = []
    functions_id: list[list[int]] = []
    function_descriptions: list[str] = []
    all_functions_id: list[int] = []
    prompts: list[str] = []
    first_prompt: str = ""
    end_prompt: str = (
        "\nBased on the intended action above, "
        "the correct matching function is: "
    )
    final_prompt: str = ""
    result: dict[str, list[str | list[str]]] = {}

    _max_tokens: list[int | float] = PrivateAttr(default_factory=list)
    _ids_token: list[float] = PrivateAttr(default_factory=list)
    _need_break: bool = PrivateAttr(default=False)
    _encode_prompt: list[int] = PrivateAttr(default_factory=list)
    _ids_prompt: list[float] = PrivateAttr(default_factory=list)
    _functions_id_valid: list[list[int]] = PrivateAttr(
        default_factory=list
    )
    _max_score: float = PrivateAttr(default=0)
    _max_token: int | float = PrivateAttr(default=0)
    
    def function_response(self) -> dict[str, list[str | list[str]]]:
        """Search for each prompt a compatible function name

        Returns:
            dict[str, str]: key = prompt and value = function's name
        """

        self.get_functions_info()
        self.get_prompts()
        self.construct_prompt()

        max_len = max([len(ids) for ids in self.functions_id])

        for prompt in self.prompts:

            self.final_prompt = self.first_prompt + \
                                prompt + "\n" + \
                                self.end_prompt

            self._max_tokens: list[int | float] = []
            self._ids_token: list[float] = []

            self._need_break: bool = False

            self._encode_prompt = self.llm.encode(
                self.final_prompt).tolist()[0]

            self._ids_prompt = self.llm.get_logits_from_input_ids(
                self._encode_prompt)

            self.get_valid_function(max_len)

            self.final_prompt = self.llm.decode(self._encode_prompt)

            self.recup_result()

        return self.result

    def get_functions_info(self) -> None:
        """Get the name and the description for each function
        """

        functions = self.json_data.get("functions", [])

        for function in functions:
            self.functions_names.append(function.get("name", ""))
            self.function_descriptions.append(function.get("description", ""))

        for name in self.functions_names:
            self.functions_id.append(self.llm.encode(name).tolist()[0])
            self.all_functions_id.extend(self.llm.encode(name).tolist()[0])

    def get_prompts(self) -> None:
        """Get all prompts

        Returns:
            list: all prompts
        """

        prompts = self.json_data.get("prompts", [])

        for prompt in prompts:
            self.prompts.append(prompt.get("prompt", ""))

    def construct_prompt(self) -> None:
        """Construct a prompt with name and descrition functions
        """

        self.first_prompt = (
            "You are a function-calling assistant. Below is a list of "
            "available functions, each with a name and description.\n\n")

        for i, name in enumerate(self.functions_names):
            self.first_prompt += f"Function {i}: {name} " \
                                f"-> {self.function_descriptions[i]} \n"

        self.first_prompt += (
            "\nRead the user prompt carefully and identify the action "
            "the user actually wants performed. Do not select a function "
            "just because a word in its name also appears in the prompt "
            "text — focus on the intended operation, not surface wording.\n\n"
            "User prompt: ")

    def get_valid_function(self, max_len: int) -> None:
        """Compare functions with prompt to keep only
           possible functions depending on prompt

        Args:
            max_len (_type_): length of the longest
                              token list for the functions
        """

        for nbr in range(max_len):

            self._functions_id_valid: list[list[int]] = []

            ids_prompt = self.llm.get_logits_from_input_ids(
                self._encode_prompt)

            self.determines_valid_function()

            if self._need_break is True:
                self.final_prompt = self.llm.decode(self._encode_prompt)
                break

            ids_token = self.search_token(ids_prompt, nbr)

            self._max_score = max([score[0] for score in ids_token])
            self._max_token = next(tok[1] for tok in ids_token
                                  if tok[0] == self._max_score)
            self._max_tokens.append(self._max_token)
            self._encode_prompt.append(self._max_token)

    def search_token(self, ids_prompt: list[float],
                     nbr: int) -> list[list[float | int]]:

        ids_token = []

        for tokens in self._functions_id_valid:
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
            if self._max_tokens == []:
                self._functions_id_valid.append(tokens)

            else:
                verif: bool = False
                for tok in self._max_tokens:
                    if tok in tokens:
                        verif = True
                    else:
                        verif = False
                        break
                if verif is True:
                    self._functions_id_valid.append(tokens)

        if len(self._functions_id_valid) == 1:
            for id in self.functions_id:
                if id == self._functions_id_valid[0]:
                    last_token = id.index(self._encode_prompt[-1]) + 1
                    try:
                        for token in id[last_token:]:
                            self._encode_prompt.append(token)
                    except IndexError:
                        pass
                    self._need_break = True
                    break

    def recup_result(self) -> None:
        """Matches the prompt with the expected function name
        """

        prompt = self.final_prompt.split("User prompt: ")[1].split("\n")[0]
        function = self.final_prompt.split(
            "matching function is: ")[1].split("\n")[0].strip()

        self.result[prompt] = [function]
