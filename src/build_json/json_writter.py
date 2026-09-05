# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  json_writter.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/26 13:39:42 by agathe          #+#    #+#               #
#  Updated: 2026/09/05 17:25:52 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import json


class JsonWritten:

    def create_json(self, functions_parameters: list[dict[str, str]]) -> None:
        """Create JSON output

        Args:
            functions_parameters (list[dict[str, str]]): all prompt with
            it function's name and parameters
        """

        try:

            with open(sys.argv[3], "w") as write:
                json.dump(functions_parameters, write, indent=4)
                print(f"\nYou can open {sys.argv[3]}, that's ready ! :)\n")

        except FileNotFoundError:
            print("ERROR: function calling results file not found")
            sys.exit()
        except PermissionError:
            print("ERROR: function calling results file denied permission")
            sys.exit()
