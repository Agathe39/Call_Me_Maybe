# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/08/31 14:16:11 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# from src.decoding.function_calling import FunctionCalling
# from src.decoding.parameters import Parameters
# from src.build_json.json_writter import JsonWritten
# from llm_sdk import Small_LLM_Model


from src.read_json.collect_json import CollectJson
# from src.test.test_llm import TestLlm
import sys


def main() -> None:

    # llm = Small_LLM_Model()

    input_functions = CollectJson()
    functions = input_functions.collect_input_functions(sys.argv[0])
    
    input_prompts = CollectJson()
    prompts = input_prompts.collect_input_prompts(sys.argv[1])

    

    # search_name = FunctionCalling(llm)
    # functions_names = search_name.function_response()

    # test = TestLlm(llm, functions_names)
    # functions_parameters = test.generate_test()
    
    # search_parameters = Parameters(llm, functions_names)
    # functions_parameters = search_parameters.parameters_calling()

    # create_json = JsonWritten()
    # create_json.write_output(functions_parameters)


if __name__ == "__main__":
    main()
