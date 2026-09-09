# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_functions.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 13:47:06 by agathe          #+#    #+#               #
#  Updated: 2026/09/09 18:14:39 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, model_validator
from typing import Any
from typing_extensions import Self


class InputFunctions(BaseModel):
    path: str = Field(default="")
    functions: list[dict[Any, Any]] = Field(default=[])

    @model_validator(mode="after")
    def check_data(self) -> Self:

        for function in self.functions:
            for i, (key, value) in enumerate(function.items()):

                if isinstance(key, str) is False:
                    raise ValueError(f"ERROR in {self.path}: " +
                                     "expected string for all keys")

                if (key not in ("parameters", "returns")
                        and isinstance(value, str) is False):
                    raise ValueError(f"ERROR in {self.path}: " +
                                     "expected string for all values")

                if i == 0 and key != "name":
                    raise ValueError(f"ERROR in {self.path}: " +
                                     "expected key 'name' at position 1, " +
                                     f"got '{key}'")

                elif i == 1 and key != "description":
                    raise ValueError(f"ERROR in {self.path}: " +
                                     "expected key 'description' " +
                                     f"at position 2, got '{key}'")

                elif i == 2 and key != "parameters":
                    raise ValueError(f"ERROR in {self.path}: " +
                                     "expected key 'parameters' at " +
                                     f"position 3, got '{key}'")

                elif i == 3 and key != "returns":
                    raise ValueError(f"ERROR in {self.path}: " +
                                     "expected key 'return' at " +
                                     f"position 4, got '{key}'")

                if key == "parameters":

                    for param, types in value.items():
                        if isinstance(param, str) is False:
                            raise ValueError(f"ERROR in {self.path}: "
                                             "all parameters name must "
                                             "be string")
                        for type, val in types.items():
                            if type != "type":
                                raise ValueError(f"ERROR in {self.path}:" +
                                                 "expected key 'type' at " +
                                                 "position 4 in parameters," +
                                                 f"got '{type}'")
                            if isinstance(val, str) is False:
                                raise ValueError(f"ERROR in {self.path}: "
                                                 "parameters indication type "
                                                 "must be str")

        return self
