from readgrammar import *

def CFG_to_CNF(CFG):
    # Assigning heads and bodies to the list
    h_list = list(CFG.keys())
    b_list = list(CFG.values())
    # Assigning start symbol
    startSymbol = h_list[0]

    # making new production if there is -> S (producing start symbol)
    new_production = False
    for values in b_list:
        for value in values:
            if (startSymbol in value):
                new_production = True
        if (new_production):
            break

    if new_production:
        new = {"START" : [[startSymbol]]}
        new.update(CFG)
        CFG = new
    

    # remove the unit production 
    unit_production = True
    while unit_production:
        unit_production = False
        unit = {}
        # listing all the unit production to unit
        for head, body in CFG.items():
            for variables in body:
                if (len(variables) == 1 and is_variable(variables[0])): 
                    unit_production = True
                    if (head not in unit.keys()):
                        unit[head] = [[variables[0]]]
                    else:
                        unit[head].append([variables[0]])

        # adding the production of the unit variable to their head
        for head_unit, body_unit in unit.items():
            for variable_unit in body_unit:
                for head, body in CFG.items():
                    if head == variable_unit[0] and len(variable_unit) == 1:
                        if head_unit not in CFG.keys():
                            CFG[head_unit] = body
                        else:
                            for variables in body: 
                                if variables not in CFG[head_unit]:
                                    CFG[head_unit].append(body)

        # removing the unit production from the body of CFG
        for head_unit, body_unit in unit.items():
            for variables in body_unit:
                # if len(variable_unit) == 1: gak usah kan udah di awal jadi yang ada di unit udah pasti panjang 1
                CFG[head_unit].remove(variables)
            
        # changing all the body to contain two piece
        new = {}
        delete = {}
        
        i = 0
        for head, body in CFG.items():
            for variables in body:
                symbol_head = head
                temp_variables = [v for v in variables]
                if (len(temp_variables) > 2):
                    while(len(temp_variables) > 2):
                        new_symbol = f"N{i}"
                        if symbol_head not in new.keys():
                            new[symbol_head] = [[temp_variables[0], new_symbol]] 
                        else:
                            new[symbol_head].append([temp_variables[0], new_symbol])                
                        symbol_head = new_symbol
                        temp_variables.remove(temp_variables[0])
                        i += 1

                    if symbol_head not in new.keys():
                        new[symbol_head] = [temp_variables]
                    else: 
                        new[symbol_head].append([temp_variables])
                    
                    if head not in delete.keys():
                        delete[head] = [variables]
                    else: 
                        delete[head].append([variables])

        for new_head, new_body in new.items():
            if new_head not in CFG.keys():
                CFG[new_head] = [new_body]
            else:
                CFG[new_head].extend([new_body])
        
        for delete_head, delete_body in delete.items():
            for delete_variable in delete_body:
                CFG[delete_head].remove(delete_variable)

        # Example condition now: 
        # A -> aBBB | AAA 
        # to
        # A -> aC | AD
        # D -> AA
        # C -> BE
        # E -> BB

        # replace terminal next to variable or replace the terminal with variable
        new = {}
        delete = {} 

        j = 0
        k = 0

        for head, body in CFG.items():
            for variables in body:
                if is_terminal(variables[0]) and is_terminal(variables[1]):
                    new_symbol_1 = f"P{j}"
                    new_symbol_2 = f"Q{k}"
                    
                    if head not in new.keys():
                        new[head] = [[new_symbol_1, new_symbol_2]]
                    else: 
                        new[head].append([new_symbol_1, new_symbol_2])

                    new[new_symbol_1] = [[variables[0]]]
                    new[new_symbol_2] = [[variables[1]]]

                    if head not in delete.keys():
                        delete[head] = [variables]
                    else: 
                        delete[head].append([variables])

                elif is_terminal(variables[0]) and is_variable(variables[1]):
                    new_symbol = f"P{j}"

                    if head not in new.keys():
                        new[head] = [new_symbol, variables[1]]
                    else:
                        new[head].append([new_symbol, variables[1]])

                    new[new_symbol] = [[variables[0]]]

                    if head not in delete.keys():
                        delete[head] = [variables]
                    else:
                        delete[head].append([variables])
                    
                    j += 1
                elif is_variable(variables[0]) and is_terminal(variables[1]):
                    new_symbol = f"Q{k}"

                    if head not in new.keys():
                        new[head] = [[variables[0], new_symbol]]
                    else:
                        new[head].append([variables[0], new_symbol]) 

                    new[new_symbol] = [[variables[1]]]

                    if head not in delete.keys():
                        delete[head] = [variables]
                    else:
                        delete[head].append([variables])

        # adding new production 
        for new_head, new_body in new.items():
            if new_head not in CFG.keys():
                CFG[new_head] = [new_body]
            else:
                CFG[new_head].extend(new_body)

        # deleting the old production
        for delete_head, delete_body in delete.keys():
            if delete_head not in CFG.keys():
                CFG[delete_head] = [delete_body]
            else:
                CFG[delete_head].remove(delete_body) 

    return CFG