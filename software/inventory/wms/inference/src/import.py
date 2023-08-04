import numpy as np
import datetime
import time
import sqlite3

start_time = time.time()
text_time = time.strftime("%Y%m%d%H%M%S", time.localtime(start_time))

this_file_name = "generate_process.py"
db_file_name = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/inference/csv/inference.db"
import_file_name = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/db.sqlite3"

db_product = "db_product"
db_order = "db_order"
db_data = "db_data"
db_statistic = "db_statistic"
db_all_statistic = "db_all_statistic"

print("d")

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

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
    carrier_stored_timestamp.append(datetime.datetime.strptime(row[4], '%Y-%m-%d').strftime('%Y-%m-%d'))
    carrier_despatch_timestamp.append(datetime.datetime.strptime(row[5], '%Y-%m-%d').strftime('%Y-%m-%d'))
    carrier_shelf_age.append(int(row[6]))

carrier_id = np.array(carrier_id)
carrier_order_code = np.array(carrier_order_code)
carrier_carrier_code = np.array(carrier_carrier_code)
carrier_product_code = np.array(carrier_product_code)
carrier_stored_timestamp = np.array(carrier_stored_timestamp)
carrier_despatch_timestamp = np.array(carrier_despatch_timestamp)
carrier_shelf_age = np.array(carrier_shelf_age)

print(carrier_shelf_age)

conn = sqlite3.connect(import_file_name)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS controller_carrier (
                id INTEGER PRIMARY KEY,
                order_code TEXT,
                carrier_code TEXT,
                product_code TEXT,
                stored_timestamp TEXT,
                despatch_timestamp TEXT,
                shelf_age INTEGER
               )''')
cursor.execute('DELETE FROM controller_carrier')


for i in range(carrier_id.size):
    carrier_data = []
    carrier_line = (        
        carrier_id,
        carrier_order_code,
        carrier_carrier_code,
        carrier_product_code,
        carrier_stored_timestamp,
        carrier_despatch_timestamp,
        carrier_shelf_age
    )
    carrier_data.append(carrier_line)
    cursor.executemany('INSERT INTO controller_statisticC VALUES (?, ?, ?, ?, ?, ?, ?)', carrier_data)
    print(carrier_data, "\n")