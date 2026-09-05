# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_prompts.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/31 14:12:28 by agathe          #+#    #+#               #
#  Updated: 2026/09/04 10:51:52 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from xml.dom import ValidationErr
from pydantic import BaseModel, Field, model_validator
from typing import Any
from typing_extensions import Self


class InputPrompts(BaseModel):
    path: str = Field(default="")
    prompts: list[dict[Any, Any]] = Field(default=[])

    @model_validator(mode="after")
    def check_data(self) -> Self:
        for prompt in self.prompts:
            for key, value in prompt.items():
                if key != "prompt":
                    raise ValidationErr(f"\nERROR in {self.path}: expected \
                                        key 'prompt', got '{key}'\n")
                if isinstance(value, str) is False:
                    raise ValidationErr(f"\nERROR in {self.path}: expected \
                                    type value str")
        return self
