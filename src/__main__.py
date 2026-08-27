# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/08/26 14:09:12 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.decoding.function_calling import FunctionCalling
from src.decoding.parameters import Parameters
from src.build_json.json_writter import JsonWritten


def main() -> None:

    search_name = FunctionCalling()
    functions_names = search_name.function_response()

    search_parameters = Parameters(functions_names)
    functions_parameters = search_parameters.parameters_calling()

    create_json = JsonWritten()
    create_json.write_output(functions_parameters)
    

if __name__ == "__main__":
    main()
