import pandas as pd
import random

import os
os.chdir("C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/inference/csv/")

nor = 150

def ret_pos(sum_value):
    if sum_value <= 23:
        return 2
    elif sum_value > 23 and sum_value <= 25:
        return 1
    elif sum_value > 25:
        return 0
    
def generate_rules():
    # Step 1: Create dataframe with 6 columns and 3 rows
    posv = [0, 1, 2]
    values = ['high', 'medium', 'low']
    columns = ['input_variable1', 'input_variable2', 'input_variable3', 'input_variable4', 'input_variable5', 'input_variable6']
    da = {
        'input_variable1': [2, 1, 0],
        'input_variable2': [0, 0.5, 1],
        'input_variable3': [0, 0.5, 1],
        'input_variable4': [1, 0.5, 0],
        'input_variable5': [2, 1, 0],
        'input_variable6': [0.5, 0.25, 0]
    }
    db = {
        'input_variable1': [2, 1, 0],
        'input_variable2': [2, 1, 0],
        'input_variable3': [0, 0.25, 0.5],
        'input_variable4': [0, 0.25, 0.5],
        'input_variable5': [0, 0.5, 1],
        'input_variable6': [0, 1, 2]
    }
    da = pd.DataFrame(da, index=values)
    db = pd.DataFrame(db, index=values)
    sa = 0
    sb = 0
    # Step 2: Generate combinations and calculate the sum
    rules = []
    rule_counter = 0
    log_file = open("rules.csv", "w")
    while rule_counter < nor:
        rule_counter += 1

        i0 = random.sample(posv, 1)[0]
        i1 = random.sample(posv, 1)[0]
        i2 = random.sample(posv, 1)[0]
        i3 = random.sample(posv, 1)[0]
        i4 = random.sample(posv, 1)[0]
        i5 = random.sample(posv, 1)[0]

        rule_name = f"rule{rule_counter}"
        sa = da.iloc[i0,0] + da.iloc[i1,1] + da.iloc[i2,2] + da.iloc[i3,3] + da.iloc[i4,4] + da.iloc[i5,5]
        sb = db.iloc[i0,0] + db.iloc[i1,1] + db.iloc[i2,2] + db.iloc[i3,3] + db.iloc[i4,4] + db.iloc[i5,5]
        oa = values[ret_pos(sa)]
        ob = values[ret_pos(sb)]
        antecedent = f"{columns[0]}['{values[i0]}'] & {columns[1]}['{values[i1]}'] & {columns[2]}['{values[i2]}'] & {columns[3]}['{values[i3]}'] & {columns[4]}['{values[i4]}'] & {columns[5]}['{values[i5]}']"
        consequent = f"consequent=(output_variable1['{oa}'], output_variable2['{ob}'])"
        rule = f"{rule_name} = ctrl.Rule(antecedent=({antecedent}), {consequent})"
        rules.append(rule)
        
        log_file.write("{}\n".format(rule))
        log_file.write("rules.append({})\n".format(rule_name))
                            
    # Step 3: Return the array of combinations
    log_file.close()
    return rules

generate_rules()