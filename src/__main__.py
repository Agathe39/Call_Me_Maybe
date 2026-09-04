# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/09/04 10:11:09 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.decoding.function_calling import FunctionCalling
from src.decoding.parameters import Parameters
from src.build_json.json_writter import JsonWritten
from llm_sdk import Small_LLM_Model
from src.read_json.collect_json import CollectJson
import sys


def main() -> None:

    input_functions = CollectJson()
    json_data = input_functions.collect_data(sys.argv[1], sys.argv[2])

    llm = Small_LLM_Model()

    search_name = FunctionCalling(llm, json_data)
    functions_names = search_name.function_response()
    
    search_parameters = Parameters(llm, functions_names, json_data)
    functions_parameters = search_parameters.parameters_calling()

    # for prompt in functions_parameters:

    #     print()
    #     print(prompt)
    #     print()
    #     print("------------------------------")

    create_json = JsonWritten()
    create_json.create_json(functions_parameters)


if __name__ == "__main__":
    main()
