import numpy as np
import datetime
import time
import sqlite3

import os
os.chdir("C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/inference/csv/")

start_time = time.time()
text_time = time.strftime("%Y%m%d%H%M%S", time.localtime(start_time))

this_file_name = "generate_process.py"
db_file_name = "inference.db"
db_product = "db_product"
db_order = "db_order"
db_data = "db_data"
db_statistic = "db_statistic"
db_all_statistic = "db_all_statistic"

statistic_all_product_file_name = "statistic_all_carrier_" + str(text_time) + ".csv"

log_file_name = "generate_process.log"

# create log file
log_file = open(log_file_name, "w")
log_file.write("Log file for generate_statistic.py\n")
log_file.write("Start time: {}\n".format(datetime.datetime.fromtimestamp(start_time)))
log_file.close()

all_statistic_file = open(statistic_all_product_file_name, "w")
all_statistic_file.write("id,type,carrier,age,cost,price,wage,day,maxd,avgd,mind,maxf,avgf,minf,frequency")
all_statistic_file.close()

# Connect to the database (or create it if it doesn't exist)
sqldb = sqlite3.connect(db_file_name)
cursor = sqldb.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + db_all_statistic + ''' (
                id INTEGER PRIMARY KEY,
                type TEXT,
                carrier REAL,
                age REAL,
                cost REAL,
                price REAL,
                wage REAL,
                day REAL,
                maxd REAL,
                avgd REAL,
                mind REAL,
                maxf REAL,
                avgf REAL,
                minf REAL,
                frequency REAL
               )''')
cursor.execute('DELETE FROM ' + db_all_statistic)

# initialize arrays to store product data
product_id = []
product_code = []
product_quantity = []
product_cost = []
product_price = []
product_profit = []
product_wage = []

cursor.execute('SELECT * FROM ' + db_product)
product_rows = cursor.fetchall()
for row in product_rows:
    product_id.append(row[0])
    product_code.append(row[1])
    product_quantity.append(int(row[2]))
    product_cost.append(int(row[3]))
    product_price.append(int(row[4]))
    product_profit.append(int(row[5]))
    product_wage.append(int(row[6]))

product_id = np.array(product_id)
product_code = np.array(product_code)
product_quantity = np.array(product_quantity)
product_cost = np.array(product_cost)
product_price = np.array(product_price)
product_profit = np.array(product_profit)
product_wage = np.array(product_wage)

# initialize arrays to store product data
statistic_id = []
statistic_code = []
statistic_carrier = []
statistic_age = []
statistic_cost = []
statistic_price = []
statistic_wage = []
statistic_day = []
statistic_maximum_demand = []
statistic_average_demand = []
statistic_minimum_demand = []
statistic_maximum_flow = []
statistic_average_flow = []
statistic_minimum_flow = []
statistic_frequency = []

scaling_ratio = 1000

cursor.execute('SELECT * FROM ' + db_statistic)
statistic_rows = cursor.fetchall()
for row in statistic_rows:
    statistic_id.append(row[0])
    statistic_code.append(row[1])
    statistic_carrier.append(float(row[2]))
    statistic_age.append(float(row[3]))
    statistic_cost.append(float(row[4])/scaling_ratio)
    statistic_price.append(float(row[5])/scaling_ratio)
    statistic_wage.append(float(row[6])/scaling_ratio)
    statistic_day.append(float(row[8]))
    statistic_maximum_demand.append(float(row[9]))
    statistic_average_demand.append(float(row[10]))
    statistic_minimum_demand.append(float(row[11]))
    statistic_maximum_flow.append(float(row[12]))
    statistic_average_flow.append(float(row[13]))
    statistic_minimum_flow.append(float(row[14]))
    statistic_frequency.append(float(row[15]))

statistic_id = np.array(statistic_id)
statistic_code = np.array(statistic_code)
statistic_carrier = np.array(statistic_carrier)
statistic_age = np.array(statistic_age)
statistic_cost = np.array(statistic_cost)
statistic_price = np.array(statistic_price)
statistic_wage = np.array(statistic_wage)
statistic_day = np.array(statistic_day)
statistic_maximum_demand = np.array(statistic_maximum_demand)
statistic_average_demand = np.array(statistic_average_demand)
statistic_minimum_demand = np.array(statistic_minimum_demand)
statistic_maximum_flow = np.array(statistic_maximum_flow)
statistic_average_flow = np.array(statistic_average_flow)
statistic_minimum_flow = np.array(statistic_minimum_flow)
statistic_frequency = np.array(statistic_frequency)

# log current time
current_time = time.time()
counter_time = current_time - start_time
log_file = open(log_file_name, "a")
log_file.write("Process time: {}\n".format(datetime.datetime.fromtimestamp(current_time)))
log_file.write("Process elapsed in: {} seconds\n".format(counter_time))
log_file.close()

# calculate overall statistics
sum_carrier = np.sum(statistic_carrier)
sum_age = np.sum(statistic_age)
sum_cost = np.sum(statistic_cost)*scaling_ratio
sum_price = np.sum(statistic_price)*scaling_ratio
sum_wage = np.sum(statistic_wage)*scaling_ratio
sum_day = np.sum(statistic_day)
sum_maximum_demand = np.sum(statistic_maximum_demand)
sum_average_demand = np.sum(statistic_average_demand)
sum_minimum_demand = np.sum(statistic_minimum_demand)
sum_maximum_flow = np.sum(statistic_maximum_flow)
sum_average_flow = np.sum(statistic_average_flow)
sum_minimum_flow = np.sum(statistic_minimum_flow)
sum_frequency = np.sum(statistic_frequency)

max_carrier = np.max(statistic_carrier)
max_age = np.max(statistic_age)
max_cost = np.max(statistic_cost)*scaling_ratio
max_price = np.max(statistic_price)*scaling_ratio
max_wage = np.max(statistic_wage)*scaling_ratio
max_day = np.max(statistic_day)
max_maximum_demand = np.max(statistic_maximum_demand)
max_average_demand = np.max(statistic_average_demand)
max_minimum_demand = np.max(statistic_minimum_demand)
max_maximum_flow = np.max(statistic_maximum_flow)
max_average_flow = np.max(statistic_average_flow)
max_minimum_flow = np.max(statistic_minimum_flow)
max_frequency = np.max(statistic_frequency)

avg_carrier = np.average(statistic_carrier)
avg_age = np.average(statistic_age)
avg_cost = np.average(statistic_cost)*scaling_ratio
avg_price = np.average(statistic_price)*scaling_ratio
avg_wage = np.average(statistic_wage)*scaling_ratio
avg_day = np.average(statistic_day)
avg_maximum_demand = np.average(statistic_maximum_demand)
avg_average_demand = np.average(statistic_average_demand)
avg_minimum_demand = np.average(statistic_minimum_demand)
avg_maximum_flow = np.average(statistic_maximum_flow)
avg_average_flow = np.average(statistic_average_flow)
avg_minimum_flow = np.average(statistic_minimum_flow)
avg_frequency = np.average(statistic_frequency)

med_carrier = np.median(statistic_carrier)
med_age = np.median(statistic_age)
med_cost = np.median(statistic_cost)*scaling_ratio
med_price = np.median(statistic_price)*scaling_ratio
med_wage = np.median(statistic_wage)*scaling_ratio
med_day = np.median(statistic_day)
med_maximum_demand = np.median(statistic_maximum_demand)
med_average_demand = np.median(statistic_average_demand)
med_minimum_demand = np.median(statistic_minimum_demand)
med_maximum_flow = np.median(statistic_maximum_flow)
med_average_flow = np.median(statistic_average_flow)
med_minimum_flow = np.median(statistic_minimum_flow)
med_frequency = np.median(statistic_frequency)

min_carrier = np.min(statistic_carrier)
min_age = np.min(statistic_age)
min_cost = np.min(statistic_cost)*scaling_ratio
min_price = np.min(statistic_price)*scaling_ratio
min_wage = np.min(statistic_wage)*scaling_ratio
min_day = np.min(statistic_day)
min_maximum_demand = np.min(statistic_maximum_demand)
min_average_demand = np.min(statistic_average_demand)
min_minimum_demand = np.min(statistic_minimum_demand)
min_maximum_flow = np.min(statistic_maximum_flow)
min_average_flow = np.min(statistic_average_flow)
min_minimum_flow = np.min(statistic_minimum_flow)
min_frequency = np.min(statistic_frequency)

ptp_carrier = np.ptp(statistic_carrier)
ptp_age = np.ptp(statistic_age)
ptp_cost = np.ptp(statistic_cost)*scaling_ratio
ptp_price = np.ptp(statistic_price)*scaling_ratio
ptp_wage = np.ptp(statistic_wage)*scaling_ratio
ptp_day = np.ptp(statistic_day)
ptp_maximum_demand = np.ptp(statistic_maximum_demand)
ptp_average_demand = np.ptp(statistic_average_demand)
ptp_minimum_demand = np.ptp(statistic_minimum_demand)
ptp_maximum_flow = np.ptp(statistic_maximum_flow)
ptp_average_flow = np.ptp(statistic_average_flow)
ptp_minimum_flow = np.ptp(statistic_minimum_flow)
ptp_frequency = np.ptp(statistic_frequency)

std_carrier = np.std(statistic_carrier)
std_age = np.std(statistic_age)
std_cost = np.std(statistic_cost)*scaling_ratio
std_price = np.std(statistic_price)*scaling_ratio
std_wage = np.std(statistic_wage)*scaling_ratio
std_day = np.std(statistic_day)
std_maximum_demand = np.std(statistic_maximum_demand)
std_average_demand = np.std(statistic_average_demand)
std_minimum_demand = np.std(statistic_minimum_demand)
std_maximum_flow = np.std(statistic_maximum_flow)
std_average_flow = np.std(statistic_average_flow)
std_minimum_flow = np.std(statistic_minimum_flow)
std_frequency = np.std(statistic_frequency)

var_carrier = np.var(statistic_carrier)
var_age = np.var(statistic_age)
var_cost = np.var(statistic_cost)*scaling_ratio
var_price = np.var(statistic_price)*scaling_ratio
var_wage = np.var(statistic_wage)*scaling_ratio
var_day = np.var(statistic_day)
var_maximum_demand = np.var(statistic_maximum_demand)
var_average_demand = np.var(statistic_average_demand)
var_minimum_demand = np.var(statistic_minimum_demand)
var_maximum_flow = np.var(statistic_maximum_flow)
var_average_flow = np.var(statistic_average_flow)
var_minimum_flow = np.var(statistic_minimum_flow)
var_frequency = np.var(statistic_frequency)

# write overall statistics to file
sum_data = []
sum_line = (
    '1',
    'sum',        
    sum_carrier,
    sum_age,
    sum_cost,
    sum_price,
    sum_wage,
    sum_day,
    sum_maximum_demand,
    sum_average_demand,
    sum_minimum_demand,
    sum_maximum_flow,
    sum_average_flow,
    sum_minimum_flow,
    sum_frequency
)
sum_data.append(sum_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sum_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '1',
    'sum',
    sum_carrier,
    sum_age,
    sum_cost,
    sum_price,
    sum_wage,
    sum_day,
    sum_maximum_demand,
    sum_average_demand,
    sum_minimum_demand,
    sum_maximum_flow,
    sum_average_flow,
    sum_minimum_flow,
    sum_frequency
))

max_data = []
max_line = (
    '2',
    'max',        
    max_carrier,
    max_age,
    max_cost,
    max_price,
    max_wage,
    max_day,
    max_maximum_demand,
    max_average_demand,
    max_minimum_demand,
    max_maximum_flow,
    max_average_flow,
    max_minimum_flow,
    max_frequency
)
max_data.append(max_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', max_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '2',
    'max',  
    max_carrier,
    max_age,
    max_cost,
    max_price,
    max_wage,
    max_day,
    max_maximum_demand,
    max_average_demand,
    max_minimum_demand,
    max_maximum_flow,
    max_average_flow,
    max_minimum_flow,
    max_frequency
))

avg_data = []
avg_line = (
    '3',
    'avg',        
    avg_carrier,
    avg_age,
    avg_cost,
    avg_price,
    avg_wage,
    avg_day,
    avg_maximum_demand,
    avg_average_demand,
    avg_minimum_demand,
    avg_maximum_flow,
    avg_average_flow,
    avg_minimum_flow,
    avg_frequency
)
avg_data.append(avg_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', avg_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '3',
    'avg',  
    avg_carrier,
    avg_age,
    avg_cost,
    avg_price,
    avg_wage,
    avg_day,
    avg_maximum_demand,
    avg_average_demand,
    avg_minimum_demand,
    avg_maximum_flow,
    avg_average_flow,
    avg_minimum_flow,
    avg_frequency
))

med_data = []
med_line = (
    '4',
    'med',        
    med_carrier,
    med_age,
    med_cost,
    med_price,
    med_wage,
    med_day,
    med_maximum_demand,
    med_average_demand,
    med_minimum_demand,
    med_maximum_flow,
    med_average_flow,
    med_minimum_flow,
    med_frequency
)
med_data.append(med_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', med_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '4',
    'med', 
    med_carrier,
    med_age,
    med_cost,
    med_price,
    med_wage,
    med_day,
    med_maximum_demand,
    med_average_demand,
    med_minimum_demand,
    med_maximum_flow,
    med_average_flow,
    med_minimum_flow,
    med_frequency
))

min_data = []
min_line = (
    '5',
    'min',        
    min_carrier,
    min_age,
    min_cost,
    min_price,
    min_wage,
    min_day,
    min_maximum_demand,
    min_average_demand,
    min_minimum_demand,
    min_maximum_flow,
    min_average_flow,
    min_minimum_flow,
    min_frequency
)
min_data.append(min_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', min_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '5',
    'min', 
    min_carrier,
    min_age,
    min_cost,
    min_price,
    min_wage,
    min_day,
    min_maximum_demand,
    min_average_demand,
    min_minimum_demand,
    min_maximum_flow,
    min_average_flow,
    min_minimum_flow,
    min_frequency
))

ptp_data = []
ptp_line = (
    '6',
    'ran',        
    ptp_carrier,
    ptp_age,
    ptp_cost,
    ptp_price,
    ptp_wage,
    ptp_day,
    ptp_maximum_demand,
    ptp_average_demand,
    ptp_minimum_demand,
    ptp_maximum_flow,
    ptp_average_flow,
    ptp_minimum_flow,
    ptp_frequency
)
ptp_data.append(ptp_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ptp_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '6',
    'ran',  
    ptp_carrier,
    ptp_age,
    ptp_cost,
    ptp_price,
    ptp_wage,
    ptp_day,
    ptp_maximum_demand,
    ptp_average_demand,
    ptp_minimum_demand,
    ptp_maximum_flow,
    ptp_average_flow,
    ptp_minimum_flow,
    ptp_frequency
))

std_data = []
std_line = (
    '7',
    'std',        
    std_carrier,
    std_age,
    std_cost,
    std_price,
    std_wage,
    std_day,
    std_maximum_demand,
    std_average_demand,
    std_minimum_demand,
    std_maximum_flow,
    std_average_flow,
    std_minimum_flow,
    std_frequency
)
std_data.append(std_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', std_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '7',
    'std',  
    std_carrier,
    std_age,
    std_cost,
    std_price,
    std_wage,
    std_day,
    std_maximum_demand,
    std_average_demand,
    std_minimum_demand,
    std_maximum_flow,
    std_average_flow,
    std_minimum_flow,
    std_frequency
))

var_data = []
var_line = (
    '8',
    'var',        
    var_carrier,
    var_age,
    var_cost,
    var_price,
    var_wage,
    var_day,
    var_maximum_demand,
    var_average_demand,
    var_minimum_demand,
    var_maximum_flow,
    var_average_flow,
    var_minimum_flow,
    var_frequency
)
var_data.append(var_line)
cursor.executemany('INSERT INTO ' + db_all_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', var_data)

all_statistic_file = open(statistic_all_product_file_name, "a")
all_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    '8',
    'var',  
    var_carrier,
    var_age,
    var_cost,
    var_price,
    var_wage,
    var_day,
    var_maximum_demand,
    var_average_demand,
    var_minimum_demand,
    var_maximum_flow,
    var_average_flow,
    var_minimum_flow,
    var_frequency
))

all_statistic_file.close()

# Commit the changes and close the connection
sqldb.commit()
sqldb.close()

# the end is comming
end_time = time.time()
elapsed_time = end_time - start_time

log_file = open(log_file_name, "a")
log_file.write("End time: {}\n".format(datetime.datetime.fromtimestamp(end_time)))
log_file.write("Process elapsed in: {} seconds\n".format(elapsed_time))
log_file.close()