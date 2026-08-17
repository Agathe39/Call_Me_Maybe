# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/08/17 16:12:04 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.decoding.function_calling import FunctionCalling
from src.decoding.parameters import Parameters
# import data.input
# import json


def main() -> None:

    search_name = FunctionCalling()
    functions_names = search_name.function_response()
    # for prompt, function in functions_names.items():
    #     print(prompt, ":", function)

    search_parameters = Parameters()
    functions_parameters = search_parameters.parameters_calling(functions_names)
    

if __name__ == "__main__":
    main()
