import numpy as np
import csv
import def_analysis
import def_npcsv

file_in = "value.csv"
file_out = 'abc.csv'

id = def_npcsv.read_csv_column(file_in, 0)
identification = def_npcsv.read_csv_column(file_in, 1)
despatch = def_npcsv.float_read_csv_column(file_in, 2)
age = def_npcsv.float_read_csv_column(file_in, 3)
cost = def_npcsv.float_read_csv_column(file_in, 4)
wage = def_npcsv.float_read_csv_column(file_in, 5)
demand = def_npcsv.float_read_csv_column(file_in, 6)
flow = def_npcsv.float_read_csv_column(file_in,7)
order = def_npcsv.float_read_csv_column(file_in,8)

s_identification = def_npcsv.remove_spaces(identification)
abc_despatch = def_analysis.abc_analysis(despatch)
abc_age = def_analysis.abc_analysis(age)
abc_cost = def_analysis.abc_analysis(cost)
abc_wage = def_analysis.abc_analysis(wage)
abc_order = def_analysis.abc_analysis(order)

with open(file_out, 'w', newline='') as file:
    writer = csv.writer(file)
    header = ['id', 'identification', 'despatch', 'age', 'cost', 'wage', 'order', 'demand', 'flow']
    writer.writerow(header)
    for i in range(identification.size):
        line = [id[i], s_identification[i], abc_despatch[i],  abc_age[i], abc_cost[i], abc_wage[i], abc_order[i], demand[i], flow[i]]
        writer.writerow(line)

print(f"Data written to {file_out} successfully!")
