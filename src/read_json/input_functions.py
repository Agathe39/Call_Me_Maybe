# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_functions.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 13:47:06 by agathe          #+#    #+#               #
#  Updated: 2026/08/31 14:12:47 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, model_validator
from typing import Any
from typing_extensions import Self


class InputFunctions(BaseModel):
    function: list[dict[Any, Any]] = Field(default = [])

    @model_validator(mode="after") 
    def check_data(self) -> Self:
        pass