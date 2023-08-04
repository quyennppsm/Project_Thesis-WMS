import os
import csv
import numpy as np

os.chdir('C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/inference/csv/')

def remove_spaces(input_array):
    # Convert the input array to a 1D array of strings
    str_array = np.char.mod('%s', input_array)

    # Remove spaces from the string array
    no_spaces_array = np.char.replace(str_array, ' ', '')

    # Convert the string array back to the original data type
    output_array = no_spaces_array.astype(input_array.dtype)

    return output_array

def read_csv_column(file, column):
    with open(file, 'r') as valuefile:
        reader = csv.reader(valuefile)
        header = next(reader)
        v_identification_list = []
        for row in reader:
            v_identification_list.append(row[column])

    v_identification_array = np.array(v_identification_list)
    return v_identification_array

def int_read_csv_column(file, column):
    with open(file, 'r') as valuefile:
        reader = csv.reader(valuefile)
        header = next(reader)
        v_id_list = []
        for row in reader:
            v_id_list.append(int(row[column]))

    v_id_array = np.array(v_id_list)
    return v_id_array

def float_read_csv_column(file, column):
    with open(file, 'r') as valuefile:
        reader = csv.reader(valuefile)
        header = next(reader)
        v_age_list = []
        for row in reader:
            v_age_list.append(float(row[column]))

    v_age_array = np.array(v_age_list)
    return v_age_array
