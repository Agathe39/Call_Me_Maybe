# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  json_writter.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/26 13:39:42 by agathe          #+#    #+#               #
#  Updated: 2026/08/26 14:09:26 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class JsonWritten:

    def __init__(self) -> None:
        pass

    def write_output(self, functions_parameters: dict[str, list[str]]) -> None:

        for prompt, func_param in functions_parameters.items():
                print(prompt, ":")
                for item in func_param:
                    print("- ", item)
                print()
                print()