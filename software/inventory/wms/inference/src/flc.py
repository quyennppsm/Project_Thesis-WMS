import matplotlib.pyplot as plt
import numpy as np
import time, datetime
from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference
import def_npcsv
from def_analysis import seconds_to_days
import math

start_time = time.time()
print("Start: ", datetime.datetime.fromtimestamp(start_time))

# Read from csv
file_csv = "value.csv"

v_id = np.array(def_npcsv.read_csv_column(file_csv, 0))
v_identification = np.array(def_npcsv.read_csv_column(file_csv, 1))
v_despatch = np.array(def_npcsv.int_read_csv_column(file_csv, 2))
d_age = np.array(def_npcsv.int_read_csv_column(file_csv, 3))
v_cost = np.array(def_npcsv.int_read_csv_column(file_csv, 4))
v_wage = np.array(def_npcsv.int_read_csv_column(file_csv, 5))
v_order = np.array(def_npcsv.int_read_csv_column(file_csv, 8))
v_demand = np.array(def_npcsv.float_read_csv_column(file_csv, 6))
v_flow = np.array(def_npcsv.float_read_csv_column(file_csv, 7))

v_age = np.zeros_like(d_age)
for i in range(d_age.size):
    v_age[i] = seconds_to_days(d_age[i])

current_time = time.time()
print("Variables: ", datetime.datetime.fromtimestamp(current_time))

r_despatch = np.max(v_despatch) - np.min(v_despatch)
r_age = np.max(v_age) - np.min(v_age)
r_cost = np.max(v_cost) - np.min(v_cost)
r_wage = np.max(v_wage) - np.min(v_wage)
r_order = np.max(v_order) - np.min(v_order)
r_demand = np.max(v_demand) - np.min(v_demand)
r_flow = np.max(v_flow) - np.min(v_flow)

print(r_despatch, r_age, r_cost, r_wage, r_order, r_demand, r_flow)

end_time = time.time()
print(datetime.datetime.fromtimestamp(end_time))

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.5f} seconds")