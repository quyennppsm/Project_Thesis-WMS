import numpy as np
import random
import string
import datetime
import time
import sqlite3

import os
os.chdir('C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/inference/csv/')

start_time = time.time()
text_time = time.strftime("%Y%m%d%H%M%S", time.localtime(start_time))

this_file_name = "generate_data.py"
db_file_name = "inference.db"
db_product = "db_product"
db_order = "db_order"
db_data = "db_data"

order_file_name = "data_order_" + str(text_time) + ".csv"
carrier_file_name = "data_carrier_" + str(text_time) + ".csv"

log_file_name = "generate_data.log"

# initialize variables
total_item_despatched = 75982216
total_item_generated = 0

# create log file
log_file = open(log_file_name, "w")
log_file.write("Log file for {}\n".format(this_file_name))
log_file.write("Start time: {}\n".format(datetime.datetime.fromtimestamp(start_time)))
log_file.close()
print("See log: {}".format(log_file_name))

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file_name)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + db_order + ''' (
                id INTEGER PRIMARY KEY,
                order_code TEXT,
                number_of_different_product INTEGER,
                received_timestamp TEXT,
                despatch_timestamp TEXT,
                order_time INTEGER
               )''')
cursor.execute('DELETE FROM ' + db_order)
cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + db_data + ''' (
                id INTEGER PRIMARY KEY,
                order_code TEXT,
                carrier_code TEXT,
                product_code TEXT,
                stored_timestamp TEXT,
                despatch_timestamp TEXT,
                shelf_age INTEGER
               )''')
cursor.execute('DELETE FROM ' + db_data)

# initialize arrays to store product data
product_id = []
product_code = []
product_quantity = []
product_cost = []
product_price = []
product_profit = []
product_wage = []

# read data from db_product and store in arrays
cursor.execute('SELECT * FROM ' + db_product)
rows = cursor.fetchall()
for row in rows:
    product_id.append(row[0])
    product_code.append(row[1])
    product_quantity.append(int(row[2]))
    product_cost.append(int(row[3]))
    product_price.append(int(row[4]))
    product_profit.append(int(row[5]))
    product_wage.append(int(row[6]))

# convert arrays to numpy arrays
product_id = np.array(product_id)
product_code = np.array(product_code)
product_quantity = np.array(product_quantity)
product_cost = np.array(product_cost)
product_price = np.array(product_price)
product_profit = np.array(product_profit)
product_wage = np.array(product_wage)

# create output files
carrier_data_file = open(carrier_file_name, "w")
carrier_data_file.write("id,order_code,carrier_code,product_code,stored_timestamp,despatch_timestamp,shelf_age")
carrier_data_file.close()

order_data_file = open(order_file_name, "w")
order_data_file.write("id,order_code,number_of_different_product,received_timestamp,despatch_timestamp,order_time")
order_data_file.close()

# counter variables
order_counter = 0
carrier_counter = 0

# loop until total_item_generated surpasses total_item_despatched
while total_item_generated < total_item_despatched:
    order_counter += 1
    # generate random order data
    order_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    number_of_different_product = random.randint(1, len(product_code))
    received_timestamp = datetime.datetime(2019, 1, 1) + datetime.timedelta(days=random.randint(0, 364))
    despatch_timestamp = received_timestamp + datetime.timedelta(days=random.randint(0, 7))
    order_time = (despatch_timestamp - received_timestamp).days

    # send data to db
    order_data = []
    order_line = (        
        order_counter,
        order_code,
        number_of_different_product,
        received_timestamp.strftime("%Y-%m-%d"),
        despatch_timestamp.strftime("%Y-%m-%d"),
        order_time
    )
    order_data.append(order_line)
    cursor.executemany('INSERT INTO ' + db_order + ' VALUES (?, ?, ?, ?, ?, ?)', order_data)

    # write order data to file
    order_data_file = open(order_file_name, "a")
    order_data_file.write("\n{},{},{},{},{},{}".format(
        order_counter,
        order_code,
        number_of_different_product,
        received_timestamp.strftime("%Y-%m-%d"),
        despatch_timestamp.strftime("%Y-%m-%d"),
        order_time
    ))
    order_data_file.close()

    # generate carrier data for each product in the order
    for i in range(number_of_different_product):
        carrier_counter += 1
        # select a random product
        product_index = random.randint(0, len(product_code) - 1)

        # generate random carrier data
        carrier_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        stored_timestamp = despatch_timestamp - datetime.timedelta(days=random.randint(0, 30))
        shelf_age = (despatch_timestamp - stored_timestamp).days

        # send data to db
        carrier_data = []
        carrier_line = (        
            carrier_counter,
            order_code,
            carrier_code,
            product_code[product_index],
            stored_timestamp.strftime("%Y-%m-%d"),
            despatch_timestamp.strftime("%Y-%m-%d"),
            shelf_age
        )
        carrier_data.append(carrier_line)
        cursor.executemany('INSERT INTO ' + db_data + ' VALUES (?, ?, ?, ?, ?, ?, ?)', carrier_data)

        # write carrier data to file
        carrier_data_file = open(carrier_file_name, "a")
        carrier_data_file.write("\n{},{},{},{},{},{},{}".format(
            carrier_counter,
            order_code,
            carrier_code,
            product_code[product_index],
            stored_timestamp.strftime("%Y-%m-%d"),
            despatch_timestamp.strftime("%Y-%m-%d"),
            shelf_age
        ))
        carrier_data_file.close()

        # update total_item_generated
        total_item_generated += product_quantity[product_index]

    # log progress
    log_file = open(log_file_name, "a")
    log_file.write("[ID:{}| Order '{}' created | ".format(order_counter, order_code))
    log_file.write("Generated {} items | ".format(total_item_generated))
    log_file.write("Pending {} items]\n".format(total_item_despatched-total_item_generated))
    log_file.close()

# Commit the changes and close the connection
conn.commit()
conn.close()

# This is the end
current_time = time.time()
counter_time = current_time - start_time
log_file = open(log_file_name, "a")
log_file.write("Process time: {}\n".format(datetime.datetime.fromtimestamp(current_time)))
log_file.write("Process generated {} orders, {} carriers and {} items.\n".format(order_counter, carrier_counter, total_item_generated))
log_file.write("Process elapsed in: {} seconds\n".format(counter_time))
log_file.close()