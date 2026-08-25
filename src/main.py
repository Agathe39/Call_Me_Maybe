# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/08/25 13:38:26 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.decoding.function_calling import FunctionCalling
from src.decoding.parameters import Parameters


def main() -> None:

    search_name = FunctionCalling()
    functions_names = search_name.function_response()

    search_parameters = Parameters(functions_names)
    functions_parameters = search_parameters.parameters_calling()

    for prompt, func_param in functions_parameters.items():
        print(prompt, ":")
        for item in func_param:
            print("- ", item)
        print()
        print()


if __name__ == "__main__":
    main()
