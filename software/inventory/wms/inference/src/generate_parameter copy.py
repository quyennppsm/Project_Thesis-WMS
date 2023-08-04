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

import matplotlib.pyplot as plt
# Extract the trimf parameters from your original code
low_trimf = [df.loc['min', 'carrier'], df.loc['min', 'carrier'], df.loc['avg', 'carrier']]
medium_trimf = [df.loc['min', 'carrier'], df.loc['avg', 'carrier'], df.loc['max', 'carrier']]
high_trimf = [df.loc['avg', 'carrier'], df.loc['max', 'carrier'], df.loc['max', 'carrier']]

# Define the universe range
universe = np.linspace(df.loc['min', 'carrier'], df.loc['max', 'carrier'], product)

# Calculate the membership degree for each trimf
low = fuzz.trimf(universe, low_trimf)
medium = fuzz.trimf(universe, medium_trimf)
high = fuzz.trimf(universe, high_trimf)

# Plot the membership functions
plt.figure()
plt.plot(universe, low, label='low')
plt.plot(universe, medium, label='medium')
plt.plot(universe, high, label='high')
plt.title('Membership Functions for Carrier')
plt.xlabel('Value')
plt.ylabel('Membership Degree')
plt.legend()
plt.show()