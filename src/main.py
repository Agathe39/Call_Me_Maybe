# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: agathe <agathe@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/08/06 16:13:44 by agathe          #+#    #+#               #
#  Updated: 2026/08/12 17:21:49 by agathe          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from llm_sdk.llm_sdk import Small_LLM_Model
import data.input
import json

def main() -> None:
    # test = Small_LLM_Model()
    # # result = test.encode("What is the sum of 2 and 3?")
    # # code = result.tolist()[0]

    # functions_names: list[str] = []
    # function_descriptions: list[str] = []
    # # function_parameters: list[dict[str, str]] = []
    # # function_returns: list[dict[str, str]] = []
    # functions_id: list[list[int]] = []
    # try:
    #     with open("data/input/functions_definition.json", "r") as f:
    #         docs = json.load(f)
    #         for doc in docs:
    #             functions_names.append(doc.get("name"))
    #             function_descriptions.append(doc.get("description"))
    #             # function_parameters.append(doc.get("parameters"))
    #             # function_returns.append(doc.get("return"))

    #     function_prompt: str = "Functions: \n"
    #     end_prompt: str = "\nPrompt -> function's name: fn_"
    #     for i, name in enumerate(functions_names):
    #         function_prompt += f"{i}: name = {name}, " \
    #         f"description = {function_descriptions[i]}\n"
    #         # f"parameters = {function_parameters[i]}, " \
    #         # f"return = {function_returns[i]}" \

    #     # print(function_prompt)

    #     for name in functions_names:
    #         functions_id.append(test.encode(name).tolist()[0])

    #     print("\nID of all name's functions:")
    #     for i, name in enumerate(functions_names):
    #         print(name, end=": ")
    #         print(functions_id[i])
    # except PermissionError:
    #     print("ERROR: denied permission")
    #     return
    # except FileNotFoundError:
    #     print("ERROR: file not found")
    #     return


    # prompts_final: list[str] = []

    # try:
    #     with open("data/input/function_calling_tests.json", "r") as f:
    #         docs = json.load(f)
    #         for doc in docs:
    #             prompts_final.append(f"{function_prompt}Prompt = {doc.get('prompt')}. {end_prompt}")
    #     # for prompt in prompts_final:
    #     #     print(prompt)
    #     #     print()
    # except PermissionError:
    #     print("ERROR: denied permission")
    #     return
    # except FileNotFoundError:
    #     print("ERROR: file not found")
    #     return
    
    
    # print()
    # # prompts: list[str] = []
    # ids: list[float] = []
    # # result: list[int] = []
    # try:

    # #     with open("data/input/function_calling_tests.json", "r") as f:
    # #         docs = json.load(f)
    # #         for doc in docs:
    # #             prompts.append(doc.get("prompt"))

    #     score_id: dict[int, int] = {}
    #     for id in functions_id:
    #         score_id[id[1]] = 0

    #     for nbr, p in enumerate(prompts_final):
    #         print(p)
    #         id_stock = test.encode(p)
    #         ids.append(id_stock.tolist()[0])
    #         all_results = test.get_logits_from_input_ids(ids[nbr])

    #         print()
    #         for id in score_id:
    #             score_id[id] = all_results[id]
    #             # print("index id =", all_results.index(id))

    #         for id, score in score_id.items():
    #             print(id, score)

    #         print()

    #         max_score = max(score for score in score_id.values())
    #         print(max_score)
    #         win_id = next(id for id, score in score_id.items() if score == max_score)
    #         print(win_id)

    #         for nbr, id in enumerate(functions_id):
    #             if win_id in id:
    #                 function = functions_names[nbr]
    #                 print(function)


    #         print()
    # #     #     max_result = max(all_results)
    # #     #     result.append(all_results.index(max_result))
    # #     # print(result)

    # # #     print()

    # # #     for i, id in enumerate(ids):
    # # #         print(id)
    # # #         id.append(int(result[i]))
    # # #         print(id)
    # # #         print()

    # # #     for id in ids:
    # # #         print(test.decode(id))
    # except PermissionError:
    #     print("ERROR: denied permission")
    #     return
    # except FileNotFoundError:
    #     print("ERROR: file not found")
    #     return

    # print()










    # test = Small_LLM_Model()

    # functions_names: list[str] = []
    # function_descriptions: list[str] = []
    # functions_id: list[list[int]] = []
    # try:
    #     with open("data/input/functions_definition.json", "r") as f:
    #         docs = json.load(f)
    #         for doc in docs:
    #             functions_names.append(doc.get("name"))
    #             function_descriptions.append(doc.get("description"))

    #     for name in functions_names:
    #         functions_id.append(test.encode(name).tolist()[0])

    #     print("\nID of all name's functions:")
    #     for i, name in enumerate(functions_names):
    #         print(name, end=": ")
    #         print(functions_id[i])

    # except PermissionError:
    #     print("ERROR: denied permission")
    #     return
    # except FileNotFoundError:
    #     print("ERROR: file not found")
    #     return

    # # print()

    # prompts: list[str] = []
    # try:
    #     with open("data/input/function_calling_tests.json", "r") as f:
    #         docs = json.load(f)
    #         for doc in docs:
    #             prompts.append(doc.get('prompt'))

    #     for prompt in prompts:
    #         print(prompt)
    # except PermissionError:
    #     print("ERROR: denied permission")
    #     return
    # except FileNotFoundError:
    #     print("ERROR: file not found")
    #     return

    # # print()

    # functions_code: list[int] = []
    # for name in functions_names:
    #     encode = test.encode(name)
    #     functions_code.append(encode.tolist()[0])

    # for prompt in prompts:

    #     i = 0
    #     # while i <= 0:
    #     while not any(name in prompt for name in functions_names):          

    #         print("\nprompt: ", prompt)
    #         score: dict[str, list[list[int], float]] = {}
    #         for i, name in enumerate(functions_names):
    #             try:
    #                 score[name] = [functions_id[i], 0]
    #             except IndexError:
    #                 pass
                

            # print("before")
            # for key, value in score.items():
            #     print(key, ": ", value)

        # while functions_names not in prompt:            
        
            # print("\nencode prompt: ", end="")
            # tensor = test.encode(prompt)
            # token = tensor.tolist()[0]
            # print(token, "\n")

            # print()
            # pour chaque nom de fonction aller chercher le score de chaque int du token
            # add le score dans le dict
            # add le token au prompt et passer au token suivant
            # une fois toutes les fonctions passées regarder celle qui a le plus gros score

            # result = test.get_logits_from_input_ids(token)
            # print(result)

            # for name, token_score in score.items():
            #     try:
            #         f_token = token_score[0]
            #         # print("f_token: ", f_token)
            #         f_score: int = result[f_token[i]]
            #         score[name] = [f_token, f_score]
            #         # print("TEST: ", end= "")
            #         # print(f_token)
            #         # for tok in f_token:
            #         #     f_score += 
            #     except IndexError:
            #         pass   

            # print("after:")
            # max_score = max([int(value[1]) for key, value in score.items()])
            # for key, value in score.items():
            #     print(key, ": ", value)
            #     if value[1] == max_score:
            #         print(token)
            #         print(value)
            #         # print(value[0][i])
            #         # token.append(value[0][i]) 

            # # print(token)
            # print(test.decode(result))
            # i + 1
                
    




















    





    test = Small_LLM_Model()

    functions_names: list[str] = []
    functions_id: list[list[int]] = []
    all_functions_id: list[int] = []

    # je récupère les noms de fonctions et je les encode
    try:
        with open("data/input/functions_definition.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                functions_names.append(doc.get("name"))

        for name in functions_names:
            functions_id.append(test.encode(name).tolist()[0])
            all_functions_id.extend(test.encode(name).tolist()[0])

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

    print()

    # je récupère chaque prompt
    prompts: list[str] = []
    try:
        with open("data/input/function_calling_tests.json", "r") as f:
            docs = json.load(f)
            for doc in docs:
                prompts.append(doc.get('prompt'))

        for prompt in prompts:
            print(prompt)
    except PermissionError:
        print("ERROR: denied permission")
        return
    except FileNotFoundError:
        print("ERROR: file not found")
        return

    print()

    # print(all_functions_id)
    max_len = max([len(ids) for ids in functions_id])
    # print(max_len)

    print()

    for prompt in prompts:

        print(prompt)
        max_tokens: list[int] = []

        # while not any(name in prompt for name in functions_names):

        # print(prompt)

        # encode_prompt = test.encode(prompt).tolist()[0]
        # ids_prompt = test.get_logits_from_input_ids(encode_prompt)

        # ids_token: list[float] = []

        functions_id_valid: list[int] = []
        # for nbr in range(max_len):
        for nbr in range(2):

            functions_id_valid: list[int] = []

            print()
            print("nbr:", nbr)

            # ids_prompt = test.get_logits_from_input_ids(encode_prompt)

            print("max_token: ", max_tokens)
            print("valide before: ", functions_id_valid)
            print()

            for nbr, tokens in enumerate(functions_id):
                print("tokens:", tokens)
                if max_tokens == []:
                    functions_id_valid.append(tokens)

                else:
                    verif: bool = False
                    for tok in max_tokens:
                        if tok in tokens:
                            verif = True
                        else:
                            verif = False
                    if verif == True:
                        functions_id_valid.append(tokens)

                # elif max_tokens in tokens:
                #     print(functions_names[nbr])
                #     functions_id_valid.append(tokens)

            print("valide after: ", functions_id_valid)
            max_tokens.extend([8822, 43277])
                # ids_token = []
                # for tokens in functions_id:

                #     try:
                #         ids_token.append([ids_prompt[tokens[nbr]], tokens[nbr]])
                #     except IndexError:
                #         continue

                #     print()

                # print("name fonction token")   
                # for p in functions_id:
                #     print(p)
        
                # print()
                # print("ids_token:")
                # for id_tok in ids_token:
                #     print(id_tok)

                # print()

                # max_score = max([score[0] for score in ids_token])
                # max_token = next(tok[1] for tok in ids_token if tok[0] == max_score)
                # max_tokens.append(max_token)

                # print("token:", max_token, "max_score:", max_score)

                # print(encode_prompt)
                # encode_prompt.append(max_token)
                # print(encode_prompt)

                # prompt = test.decode(encode_prompt)

        print()
            

if __name__ == "__main__":
    main()