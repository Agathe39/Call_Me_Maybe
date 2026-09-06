# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  json_writter.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/26 13:39:42 by agathe          #+#    #+#               #
#  Updated: 2026/09/06 11:59:48 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel
import sys
import json
import os


class JsonWritten(BaseModel):
    """Writes the function-calling results to a JSON output file.

    Serializes the extracted function names and parameters into a
    structured JSON file.
    """

    def create_json(self,
                    functions_parameters: list[dict[str, str]],
                    output_path: str) -> None:
        """Create JSON output

        Args:
            functions_parameters (list[dict[str, str]]): all prompt with
            it function's name and parameters
        """

        file = os.path.dirname(output_path)
        if file:
            os.makedirs(file, exist_ok=True)

        try:

            with open(output_path, "w") as write:
                json.dump(functions_parameters, write, indent=4)
                print(f"\nYou can open {output_path}, that's ready ! :)\n")

        except FileNotFoundError:
            print("ERROR: function calling results file not found")
            sys.exit()
        except PermissionError:
            print("ERROR: function calling results file denied permission")
            sys.exit()
