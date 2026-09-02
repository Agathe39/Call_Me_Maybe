# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_functions.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 13:47:06 by agathe          #+#    #+#               #
#  Updated: 2026/08/31 17:24:53 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from xml.dom import ValidationErr
from pydantic import BaseModel, Field, model_validator
from typing import Any
from typing_extensions import Self


class InputFunctions(BaseModel):
    path: str = Field(default="")
    functions: list[dict[Any, Any]] = Field(default = [])

    @model_validator(mode="after") 
    def check_data(self) -> Self:

        for function in self.functions:
            for i, (key, value) in enumerate(function.items()):

                if i == 0 and key != "name":
                    raise ValidationErr(f"\nERROR in {self.path}: \
                        expected key 'name' at position 1, got '{key}'\n")
                elif i == 1 and key != "description":
                    raise ValidationErr(f"\nERROR in {self.path}: \
                        expected key 'description' at position 2,\
                                         got '{key}'\n")
                elif i == 2 and key != "parameters":
                    raise ValidationErr(f"\nERROR in {self.path}: \
                        expected key 'parameters' at position 3,\
                                         got '{key}'\n")
                elif i == 3 and key != "returns":
                    raise ValidationErr(f"\nERROR in {self.path}: \
                        expected key 'return' at position 4, got '{key}'\n")

                if key == "parameters":
                    for types in value.values():
                        for t in types:
                            if t != "type":
                                raise ValidationErr(f"\nERROR in {self.path}:\
                                                     expected key 'type' at \
                                                    position 4 in parameters,\
                                                     got '{t}'\n")
        return self
