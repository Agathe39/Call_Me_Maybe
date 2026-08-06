# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/08/06 18:46:49 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
import data.input
import json

def main() -> None:
    test = Small_LLM_Model()
    result = test.encode("What is the sum of 2 and 3?")
    code = result.tolist()[0]

    
    print()
    prompts: list[str] = []
    try:
        with open("data/input/function_calling_tests.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                prompts.append(doc.get("prompt"))
        for p in prompts:
            print(p)
    except PermissionError:
        print("ERROR: denied permission")
        return
    except FileNotFoundError:
        print("ERROR: file not found")
        return

    print()

    functions_names: list[str] = []
    try:
        with open("data/input/functions_definition.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                functions_names.append(doc.get("name"))
        for p in functions_names:
            print(p)
    except PermissionError:
        print("ERROR: denied permission")
        return
    except FileNotFoundError:
        print("ERROR: file not found")
        return

    print()
    # print(code)
    # print(result)
    # print(test.decode(result))
    with open(test.get_path_to_vocab_file()) as f:
        words = json.load(f)
        for key, value in words.items():
            print(key, ":", value)
    print()

    tokens = [int(token) for token in test.get_logits_from_input_ids(code)]
    for key, value in words.items():
        for token in tokens:
            if token == value:
                print(key)
            
    # print(test.decode(result))
    # print(test.decode([int(max(nbr for nbr in ))]))

    # print(test.get_path_to_merges_file())
    # print(test.get_path_to_tokenizer_file())


if __name__ == "__main__":
    main()