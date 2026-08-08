# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/08/08 18:30:01 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
import data.input
import json

def main() -> None:
    test = Small_LLM_Model()
    # result = test.encode("What is the sum of 2 and 3?")
    # code = result.tolist()[0]

    functions_names: list[str] = []
    function_descriptions: list[str] = []
    # function_parameters: list[dict[str, str]] = []
    # function_returns: list[dict[str, str]] = []
    functions_id: list[list[int]] = []
    try:
        with open("data/input/functions_definition.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                functions_names.append(doc.get("name"))
                function_descriptions.append(doc.get("description"))
                # function_parameters.append(doc.get("parameters"))
                # function_returns.append(doc.get("return"))

        function_prompt: str = "Functions: \n"
        end_prompt: str = "\nPrompt -> function's name: fn_"
        for i, name in enumerate(functions_names):
            function_prompt += f"{i}: name = {name}, " \
            f"description = {function_descriptions[i]}\n"
            # f"parameters = {function_parameters[i]}, " \
            # f"return = {function_returns[i]}" \

        # print(function_prompt)

        for name in functions_names:
            functions_id.append(test.encode(name).tolist()[0])

        print("\nID of all name's functions:")
        for i, name in enumerate(functions_names):
            print(name, end=": ")
            print(functions_id[i])
    except PermissionError:
        print("ERROR: denied permission")
        return
    except FileNotFoundError:
        print("ERROR: file not found")
        return


    prompts_final: list[str] = []

    try:
        with open("data/input/function_calling_tests.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                prompts_final.append(f"{function_prompt}Prompt = {doc.get('prompt')}. {end_prompt}")
        # for prompt in prompts_final:
        #     print(prompt)
        #     print()
    except PermissionError:
        print("ERROR: denied permission")
        return
    except FileNotFoundError:
        print("ERROR: file not found")
        return
    
    
    print()
    # prompts: list[str] = []
    ids: list[float] = []
    # result: list[int] = []
    try:

    #     with open("data/input/function_calling_tests.json", "r") as f:
    #         docs = json.load(f)
    #         for doc in docs:
    #             prompts.append(doc.get("prompt"))

        score_id: dict[int, int] = {}
        for id in functions_id:
            score_id[id[1]] = 0

        for nbr, p in enumerate(prompts_final):
            print(p)
            id_stock = test.encode(p)
            ids.append(id_stock.tolist()[0])
            all_results = test.get_logits_from_input_ids(ids[nbr])

            print()
            for id in score_id:
                score_id[id] = all_results[id]
                # print("index id =", all_results.index(id))

            for id, score in score_id.items():
                print(id, score)

            print()

            max_score = max(score for score in score_id.values())
            print(max_score)
            win_id = next(id for id, score in score_id.items() if score == max_score)
            print(win_id)

            for nbr, id in enumerate(functions_id):
                if win_id in id:
                    function = functions_names[nbr]
                    print(function)


            print()
    #     #     max_result = max(all_results)
    #     #     result.append(all_results.index(max_result))
    #     # print(result)

    # #     print()

    # #     for i, id in enumerate(ids):
    # #         print(id)
    # #         id.append(int(result[i]))
    # #         print(id)
    # #         print()

    # #     for id in ids:
    # #         print(test.decode(id))
    except PermissionError:
        print("ERROR: denied permission")
        return
    except FileNotFoundError:
        print("ERROR: file not found")
        return

    print()

















    # print()
    # print(code)
    # print(result)
    # print(test.decode(result))
    # with open(test.get_path_to_vocab_file()) as f:
    #     words = json.load(f)
    #     for key, value in words.items():
    #         print(key, ":", value)
    # print()

    # tokens = [int(token) for token in test.get_logits_from_input_ids(code)]
    # for key, value in words.items():
    #     for token in tokens:
    #         if token == value:
    #             print(key)
            
    # print(test.decode(result))
    # print(test.decode([int(max(nbr for nbr in ))]))

    # print(test.get_path_to_merges_file())
    # print(test.get_path_to_tokenizer_file())


if __name__ == "__main__":
    main()