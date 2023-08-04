import sqlite3
import time
import datetime
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

import os
os.chdir("C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/inference/csv/")

start_time = time.time()
text_time = time.strftime("%Y%m%d%H%M%S", time.localtime(start_time))
db_file_name = "inference.db"
db_allstats = "db_all_statistic"
db_statistic = "db_statistic"

this_program_name = "generate_parameter"
parameter_file_name = 'parameter.log'
this_file_name = this_program_name + ".py"
statistic_all_product_file_name = this_program_name + ".csv"
log_file_name = this_program_name + ".log"

# create log file
log_file = open(log_file_name, "w")
log_file.write("Log file for {}\n".format(this_file_name))
log_file.write("Start time: {}\n".format(datetime.datetime.fromtimestamp(start_time)))
log_file.close()

# constant
slots = 16800
product = 434
scaling_decimal = 10
scaling_centurial = 100
scaling_millennial = 1000
scaling_epoch = 1000000

# Connect to the SQLite database
cursor = sqlite3.connect(db_file_name)
query = 'SELECT * FROM ' + db_allstats
df = pd.read_sql_query(query, cursor)
query = 'SELECT * FROM ' + db_statistic
di = pd.read_sql_query(query,cursor)
cursor.close()

del df ['id']
del df['type']
del df ['mind']
del df['minf']

db_col_index = ['carrier', 'age', 'cost', 'price', 'wage', 'day', 'maxd', 'avgd', 'maxf', 'avgf', 'frequency', 'assign', 'priority']
db_row_index = ['sum', 'max', 'avg', 'med', 'min', 'ran', 'std', 'var', 'inc']

df=pd.DataFrame(df)
new_row = [0] * df.shape[1]
new_row_df = pd.DataFrame([new_row], columns=df.columns)
df = pd.concat([df, new_row_df], ignore_index=True)
df = pd.DataFrame(index=db_row_index, columns=df.columns, data=df.values)

df.insert(df.shape[1], db_col_index[df.shape[1]], [0]*df.shape[0])
df.insert(df.shape[1], db_col_index[df.shape[1]], [0]*df.shape[0])

#df['cost'] = df['cost'] / scaling_epoch
#df['price'] = df['price'] / scaling_epoch
##df['wage'] = df['wage'] / scaling_epoch
#df['day'] = df['day'] * scaling_decimal
#df['maxd'] = df['maxd'] * scaling_decimal
#df['mind'] = df['mind'] * scaling_decimal
#df['avgd'] = df['avgd'] * scaling_centurial
#df['maxf'] = df['maxf'] * scaling_centurial
#df['avgf'] = df['avgf'] * scaling_millennial
#df['minf'] = df['minf'] * scaling_decimal
#df['frequency'] = df['frequency'] * scaling_millennial
temp_max = (df.loc['max','maxd']+df.loc['max','maxf'])/df.loc['sum','maxf']*slots
temp_avg = (slots)/product*2
temp_min = df.loc['min','maxd']
temp_range = temp_max - temp_min
temp_var = ((temp_max - temp_avg)) + ((temp_min - temp_avg)) / 2
temp_std = math.sqrt(temp_var)
df['assign'] = [slots, temp_max, temp_avg, math.ceil(temp_avg), temp_min, temp_range, temp_std, temp_var, 0]
temp_sum = (product/ 2) * (1 + product)
temp_max = product
temp_avg = np.mean(np.arange(0,product,1))
temp_min = 1
temp_range = temp_max - temp_min
temp_var = ((temp_max - temp_avg)) + ((temp_min - temp_avg)) / 2
temp_std = math.sqrt(temp_var)
df['priority'] = [temp_sum, temp_max, temp_avg, math.ceil(product/2), 1, product, temp_std, temp_var, 0]
df.loc['inc'] = df.loc['ran'] / product

print(df)

# Input
input_variable1 = ctrl.Antecedent(np.arange(df.loc['min','carrier'],df.loc['max','carrier'],df.loc['inc','carrier']), 'input_variable1')
input_variable2 = ctrl.Antecedent(np.arange(df.loc['min','age'],df.loc['max','age'],df.loc['inc','age']), 'input_variable2')
input_variable3 = ctrl.Antecedent(np.arange(df.loc['min','cost'],df.loc['max','cost'],df.loc['inc','cost']), 'input_variable3')
input_variable4 = ctrl.Antecedent(np.arange(df.loc['min','price'],df.loc['max','price'],df.loc['inc','price']), 'input_variable4')
input_variable5 = ctrl.Antecedent(np.arange(df.loc['min','wage'],df.loc['max','wage'],df.loc['inc','wage']), 'input_variable5')
input_variable6 = ctrl.Antecedent(np.arange(df.loc['min','day'],df.loc['max','day'],df.loc['inc','day']), 'input_variable6')

# Output
output_variable1 = ctrl.Consequent(np.arange(df.loc['min','assign'],df.loc['max','assign'],df.loc['inc','assign']), 'output_variable1')
output_variable2 = ctrl.Consequent(np.arange(df.loc['min','priority'],df.loc['max','priority'],df.loc['inc','priority']), 'output_variable2')

# Membership
input_variable1['low'] = fuzz.trimf(input_variable1.universe, [df.loc['min','carrier'], df.loc['min','carrier'], df.loc['avg','carrier']])
input_variable1['medium'] = fuzz.trimf(input_variable1.universe, [df.loc['min','carrier'], df.loc['avg','carrier'], df.loc['max','carrier']])
input_variable1['high'] = fuzz.trimf(input_variable1.universe, [df.loc['avg','carrier'], df.loc['max','carrier'], df.loc['max','carrier']])

input_variable2['low'] = fuzz.trimf(input_variable2.universe, [df.loc['min','age'], df.loc['min','age'], df.loc['avg','age']])
input_variable2['medium'] = fuzz.trimf(input_variable2.universe, [df.loc['min','age'], df.loc['avg','age'], df.loc['max','age']])
input_variable2['high'] = fuzz.trimf(input_variable2.universe, [df.loc['avg','age'], df.loc['max','age'], df.loc['max','age']])

input_variable3['low'] = fuzz.trimf(input_variable3.universe, [df.loc['min','cost'], df.loc['min','cost'], df.loc['avg','cost']])
input_variable3['medium'] = fuzz.trimf(input_variable3.universe, [df.loc['min','cost'], df.loc['avg','cost'], df.loc['max','cost']])
input_variable3['high'] = fuzz.trimf(input_variable3.universe, [df.loc['avg','cost'], df.loc['max','cost'], df.loc['max','cost']])

input_variable4['low'] = fuzz.trimf(input_variable4.universe, [df.loc['min','price'], df.loc['min','price'], df.loc['avg','price']])
input_variable4['medium'] = fuzz.trimf(input_variable4.universe, [df.loc['min','price'], df.loc['avg','price'], df.loc['max','price']])
input_variable4['high'] = fuzz.trimf(input_variable4.universe, [df.loc['avg','price'], df.loc['max','price'], df.loc['max','price']])

input_variable5['low'] = fuzz.trimf(input_variable5.universe, [df.loc['min','wage'], df.loc['min','wage'], df.loc['avg','wage']])
input_variable5['medium'] = fuzz.trimf(input_variable5.universe, [df.loc['min','wage'], df.loc['avg','wage'], df.loc['max','wage']])
input_variable5['high'] = fuzz.trimf(input_variable5.universe, [df.loc['avg','wage'], df.loc['max','wage'], df.loc['max','wage']])

input_variable6['low'] = fuzz.trimf(input_variable6.universe, [df.loc['min','day'], df.loc['min','day'], df.loc['avg','day']])
input_variable6['medium'] = fuzz.trimf(input_variable6.universe, [df.loc['min','day'], df.loc['avg','day'], df.loc['max','day']])
input_variable6['high'] = fuzz.trimf(input_variable6.universe, [df.loc['avg','day'], df.loc['max','day'], df.loc['max','day']])

output_variable1['low'] = fuzz.trimf(output_variable1.universe, [df.loc['min','assign'], df.loc['min','assign'], df.loc['avg','assign']])
output_variable1['medium'] = fuzz.trimf(output_variable1.universe, [df.loc['min','assign'], df.loc['avg','assign'], df.loc['max','assign']])
output_variable1['high'] = fuzz.trimf(output_variable1.universe, [df.loc['avg','assign'], df.loc['max','assign'], df.loc['max','assign']])

output_variable2['low'] = fuzz.trimf(output_variable2.universe, [df.loc['min','priority'], df.loc['min','priority'], df.loc['avg','priority']])
output_variable2['medium'] = fuzz.trimf(output_variable2.universe, [df.loc['min','priority'], df.loc['avg','priority'], df.loc['max','priority']])
output_variable2['high'] = fuzz.trimf(output_variable2.universe, [df.loc['avg','priority'], df.loc['max','priority'], df.loc['max','priority']])

# Rules
rules = []
rule1 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule1)
rule2 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule2)
rule3 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule3)
rule4 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule4)
rule5 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule5)
rule6 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule6)
rule7 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule7)
rule8 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule8)
rule9 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule9)
rule10 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule10)
rule11 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule11)
rule12 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule12)
rule13 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule13)
rule14 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule14)
rule15 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule15)
rule16 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule16)
rule17 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule17)
rule18 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule18)
rule19 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule19)
rule20 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['low'] & input_variable4['high'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule20)
rule21 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule21)
rule22 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule22)
rule23 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule23)
rule24 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule24)
rule25 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule25)
rule26 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule26)
rule27 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule27)
rule28 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule28)
rule29 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule29)
rule30 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule30)
rule31 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule31)
rule32 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['low'] & input_variable4['low'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule32)
rule33 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule33)
rule34 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule34)
rule35 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['low'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule35)
rule36 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule36)
rule37 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule37)
rule38 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule38)
rule39 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule39)
rule40 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule40)
rule41 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['high'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule41)
rule42 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule42)
rule43 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule43)
rule44 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule44)
rule45 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule45)
rule46 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule46)
rule47 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule47)
rule48 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule48)
rule49 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule49)
rule50 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['low'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule50)
rule51 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule51)
rule52 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule52)
rule53 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule53)
rule54 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule54)
rule55 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['low'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule55)
rule56 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule56)
rule57 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule57)
rule58 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule58)
rule59 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule59)
rule60 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule60)
rule61 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule61)
rule62 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule62)
rule63 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule63)
rule64 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule64)
rule65 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule65)
rule66 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule66)
rule67 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule67)
rule68 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule68)
rule69 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule69)
rule70 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['low'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule70)
rule71 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['high'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule71)
rule72 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule72)
rule73 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule73)
rule74 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule74)
rule75 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule75)
rule76 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule76)
rule77 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule77)
rule78 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule78)
rule79 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule79)
rule80 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule80)
rule81 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule81)
rule82 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['high'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule82)
rule83 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule83)
rule84 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule84)
rule85 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule85)
rule86 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule86)
rule87 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule87)
rule88 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule88)
rule89 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule89)
rule90 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule90)
rule91 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule91)
rule92 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule92)
rule93 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule93)
rule94 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule94)
rule95 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule95)
rule96 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule96)
rule97 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['high'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule97)
rule98 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule98)
rule99 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule99)
rule100 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule100)
rule101 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['low'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule101)
rule102 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule102)
rule103 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule103)
rule104 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule104)
rule105 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule105)
rule106 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['low'] & input_variable4['high'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule106)
rule107 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule107)
rule108 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule108)
rule109 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule109)
rule110 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule110)
rule111 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule111)
rule112 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule112)
rule113 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule113)
rule114 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule114)
rule115 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule115)
rule116 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule116)
rule117 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule117)
rule118 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['low'] & input_variable4['high'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule118)
rule119 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule119)
rule120 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule120)
rule121 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule121)
rule122 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule122)
rule123 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['high'] & input_variable5['low'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule123)
rule124 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule124)
rule125 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule125)
rule126 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule126)
rule127 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['high'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule127)
rule128 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule128)
rule129 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule129)
rule130 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule130)
rule131 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule131)
rule132 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule132)
rule133 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['low'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule133)
rule134 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule134)
rule135 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['high'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule135)
rule136 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule136)
rule137 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['high'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule137)
rule138 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule138)
rule139 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule139)
rule140 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['high'] & input_variable3['high'] & input_variable4['low'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule140)
rule141 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['high'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule141)
rule142 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule142)
rule143 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['high'] & input_variable3['low'] & input_variable4['low'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule143)
rule144 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['medium'] & input_variable3['low'] & input_variable4['low'] & input_variable5['high'] & input_variable6['low']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule144)
rule145 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['medium'] & input_variable4['high'] & input_variable5['high'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule145)
rule146 = ctrl.Rule(antecedent=(input_variable1['medium'] & input_variable2['medium'] & input_variable3['medium'] & input_variable4['low'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule146)
rule147 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule147)
rule148 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['medium'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['medium'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule148)
rule149 = ctrl.Rule(antecedent=(input_variable1['high'] & input_variable2['low'] & input_variable3['low'] & input_variable4['high'] & input_variable5['high'] & input_variable6['medium']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule149)
rule150 = ctrl.Rule(antecedent=(input_variable1['low'] & input_variable2['low'] & input_variable3['high'] & input_variable4['medium'] & input_variable5['low'] & input_variable6['high']), consequent=(output_variable1['low'], output_variable2['low']))
rules.append(rule150)

log_file = open(log_file_name, "a")
log_file.write("{} rules read.\n".format(int(len(rules))))
log_file.close()

# Controller
fuzzy_ctrl = ctrl.ControlSystem(rules)

log_file = open(log_file_name, "a")
log_file.write("Control system.\n")
log_file.close()

# Simulation
simulation = ctrl.ControlSystemSimulation(fuzzy_ctrl)

log_file = open(log_file_name, "a")
log_file.write("Simulate system.\n")
log_file.close()

sum_assign = 0
sum_priority = 0

# create parameter file
parameter_file = open(parameter_file_name, "w")
parameter_file.write("Parameter log file for {}\n".format(this_file_name))
parameter_file.close()

for i in range(di.shape[0]):
    # Provide
    simulation.input['input_variable1'] = di.iloc[i,2]
    simulation.input['input_variable2'] = di.iloc[i,3]
    simulation.input['input_variable3'] = di.iloc[i,4]
    simulation.input['input_variable4'] = di.iloc[i,5]
    simulation.input['input_variable5'] = di.iloc[i,6]
    simulation.input['input_variable6'] = di.iloc[i,8]

    parameter_file = open(parameter_file_name, "a")
    parameter_file.write("Compute [{}]: ".format(i))
    parameter_file.close()

    simulation.compute()

    output_value1 = simulation.output['output_variable1']
    output_value1 = math.ceil(output_value1 / 5)*5
    output_value2 = simulation.output['output_variable2']

    sum_assign += output_value1
    sum_priority += output_value2

    parameter_file = open(parameter_file_name, "a")
    parameter_file.write("{}, {}, {}, {}\n".format(di.iloc[i,0], di.iloc[i,1], output_value1, output_value2))
    parameter_file.close()

end_time = time.time()
elapsed_time = end_time - start_time
log_file = open(log_file_name, "a")
log_file.write("{} slots allocated.\n".format(sum_assign))
log_file.write("Priority check sum: {}.\n".format(sum_priority))
log_file.write("Elsaped time: {}\n".format(elapsed_time))
log_file.close()