# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/09/06 11:59:33 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.decoding.function_calling import FunctionCalling
from src.decoding.parameters import Parameters
from src.build_json.json_writter import JsonWritten
from llm_sdk import Small_LLM_Model
from src.read_json.collect_json import CollectJson
import argparse


def main() -> None:

    try:

        parser = argparse.ArgumentParser(description="paths to JSON")
        parser.add_argument(
            "--functions_definition",
            default="data/input/functions_definition.json")
        parser.add_argument(
            "--input",
            default="data/input/function_calling_tests.json")
        parser.add_argument(
            "--output",
            default="data/output/function_calling_results.json")
        args = parser.parse_args()

        input_functions = CollectJson()
        json_data = input_functions.collect_data(args.functions_definition,
                                                 args.input)

        print("Load the LLM:")
        llm = Small_LLM_Model()

        search_name = FunctionCalling(llm=llm, json_data=json_data)
        functions_names = search_name.function_response()

        search_parameters = Parameters(llm=llm,
                                       functions_names=functions_names,
                                       json_data=json_data)
        functions_parameters = search_parameters.parameters_calling()

        create_json = JsonWritten()
        create_json.create_json(functions_parameters, args.output)

    except KeyboardInterrupt:
        print("\nERROR: you have interrupted the program")


if __name__ == "__main__":
    main()
