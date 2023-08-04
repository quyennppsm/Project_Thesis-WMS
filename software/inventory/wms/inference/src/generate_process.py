import math
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

statistic_product_file_name = "statistic_carrier_" + str(text_time) + ".csv"

log_file_name = "generate_process.log"

# create log file
log_file = open(log_file_name, "w")
log_file.write("Log file for generate_record.py\n")
log_file.write("Start time: {}\n".format(datetime.datetime.fromtimestamp(start_time)))
log_file.close()
print("See log: {}".format(log_file_name))

product_statistic_file = open(statistic_product_file_name, "w")
product_statistic_file.write("id,product_code,total_carrier,total_shelf_age,total_cost,total_price,total_wage,total_order,total_different_day_timestamp,maximum_demand,average_demand,minimum_demand,maximum_flow,average_flow,minimum_flow,frequency")
product_statistic_file.close()

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file_name)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + db_statistic + ''' (
                id INTEGER PRIMARY KEY,
                product_code TEXT,
                total_carrier INTEGER,
                total_shelf_age INTEGER,
                total_cost INTEGER,
                total_price INTEGER,
                total_wage INTEGER,
                total_order INTEGER,
                total_different_day_timestamp INTEGER,
                maximum_demand INTEGER,
                average_demand REAL,
                minimum_demand INTEGER,
                maximum_flow INTEGER,
                average_flow REAL,
                minimum_flow INTEGER,
                frequency REAL)''')
cursor.execute('DELETE FROM ' + db_statistic)

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
carrier_id = []
carrier_order_code = []
carrier_carrier_code = []
carrier_product_code = []
carrier_stored_timestamp = []
carrier_despatch_timestamp = []
carrier_shelf_age = []

cursor.execute('SELECT * FROM ' + db_data)
carrier_rows = cursor.fetchall()

for row in carrier_rows:
    carrier_id.append(row[0])
    carrier_order_code.append(row[1])
    carrier_carrier_code.append(row[2])
    carrier_product_code.append(row[3])
    carrier_stored_timestamp.append(datetime.datetime.strptime(row[4], '%Y-%m-%d'))
    carrier_despatch_timestamp.append(datetime.datetime.strptime(row[5], '%Y-%m-%d'))
    carrier_shelf_age.append(int(row[6]))

    log_file = open(log_file_name, "a")
    log_file.write("[DB | Read from {} in {}: {}]\n".format(db_data, db_file_name, row))
    log_file.close()

carrier_id = np.array(carrier_id)
carrier_order_code = np.array(carrier_order_code)
carrier_carrier_code = np.array(carrier_carrier_code)
carrier_product_code = np.array(carrier_product_code)
carrier_stored_timestamp = np.array(carrier_stored_timestamp)
carrier_despatch_timestamp = np.array(carrier_despatch_timestamp)
carrier_shelf_age = np.array(carrier_shelf_age)

# calculate product statistics
product_statistic = []
maximum_demand = {}
minimum_demand = {}
maximum_flow = {}
minimum_flow = {}
scaling_factor = 1000  # Adjust the scaling factor as needed

current_time = time.time()
counter_time = current_time - start_time
log_file = open(log_file_name, "a")
log_file.write("Process time: {}\n".format(datetime.datetime.fromtimestamp(current_time)))
log_file.write("Process elapsed in: {} seconds\n".format(counter_time))
log_file.close()

for i in range(len(product_code)):
    # calculate total_carrier and total_shelf_age
    carrier_indices = np.where(carrier_product_code == product_code[i])[0]
    total_carrier = len(carrier_indices)
    total_shelf_age = np.sum(carrier_shelf_age[carrier_indices] / scaling_factor)
    total_shelf_age = math.ceil(total_shelf_age * scaling_factor)

    # calculate total_cost, total_price, and total_wage
    scaled_product_cost = product_cost[i] / scaling_factor
    scaled_product_price = product_price[i] / scaling_factor
    total_cost = total_carrier * scaled_product_cost
    total_price = total_carrier * scaled_product_price
    total_cost = math.ceil(total_cost * scaling_factor)
    total_price = math.ceil(total_price * scaling_factor)
    total_wage = total_price - total_cost

    # calculate total_order and total_different_day_timestamp
    order_indices = np.unique(carrier_order_code[carrier_indices], return_index=True)[1]
    total_order = len(order_indices)
    total_different_day_timestamp = len(np.unique(carrier_despatch_timestamp[carrier_indices]))

    # calculate maximum_demand, minimum_demand, maximum_flow, minimum_flow
    demand_dict = {}
    flow_dict = {}
    for j in range(len(carrier_indices)):
        date_str = carrier_despatch_timestamp[carrier_indices][j].strftime("%Y-%m-%d")
        if date_str in demand_dict:
            demand_dict[date_str] += 1
        else:
            demand_dict[date_str] = 1
        if carrier_order_code[carrier_indices][j] in flow_dict:
            flow_dict[carrier_order_code[carrier_indices][j]] += 1
        else:
            flow_dict[carrier_order_code[carrier_indices][j]] = 1
    max_demand_date = max(demand_dict, key=demand_dict.get)
    min_demand_date = min(demand_dict, key=demand_dict.get)
    max_flow_order = max(flow_dict, key=flow_dict.get)
    min_flow_order = min(flow_dict, key=flow_dict.get)
    maximum_demand[product_code[i]] = demand_dict[max_demand_date]
    minimum_demand[product_code[i]] = demand_dict[min_demand_date]
    maximum_flow[product_code[i]] = flow_dict[max_flow_order]
    minimum_flow[product_code[i]] = flow_dict[min_flow_order]

    # calculate average_demand, average_flow, and frequency
    average_demand = total_carrier / total_different_day_timestamp
    average_flow = total_carrier / total_order
    frequency = total_different_day_timestamp / 365

    # send data to db
    carrier_data = []
    carrier_line = (        
        i+1,
        product_code[i],
        total_carrier,
        total_shelf_age,
        total_cost,
        total_price,
        total_wage,
        total_order,
        total_different_day_timestamp,
        maximum_demand[product_code[i]],
        average_demand,
        minimum_demand[product_code[i]],
        maximum_flow[product_code[i]],
        average_flow,
        minimum_flow[product_code[i]],
        frequency
    )
    carrier_data.append(carrier_line)
    cursor.executemany('INSERT INTO ' + db_statistic + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', carrier_data)

    # write product statistics to file
    product_statistic_file = open(statistic_product_file_name, "a")
    product_statistic_file.write("\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
        i+1,
        product_code[i],
        total_carrier,
        total_shelf_age,
        total_cost,
        total_price,
        total_wage,
        total_order,
        total_different_day_timestamp,
        maximum_demand[product_code[i]],
        average_demand,
        minimum_demand[product_code[i]],
        maximum_flow[product_code[i]],
        average_flow,
        minimum_flow[product_code[i]],
        frequency
    ))
    product_statistic_file.close()

    # log progress
    log_file = open(log_file_name, "a")
    log_file.write("[ID:{} | Carrier '{}' processed]\n".format(i, product_code[i]))
    log_file.close()

# Commit the changes and close the connection
conn.commit()
conn.close()

# This is the end
end_time = time.time()
elapsed_time = end_time - start_time

log_file = open(log_file_name, "a")
log_file.write("End time: {}\n".format(datetime.datetime.fromtimestamp(end_time)))
log_file.write("Process elapsed in: {} seconds\n".format(elapsed_time))
log_file.close()