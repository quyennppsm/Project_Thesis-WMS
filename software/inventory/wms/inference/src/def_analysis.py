import numpy as np
import math

def seconds_to_days(seconds):
    # Calculate number of days (rounded up)
    temp = seconds / (24 * 60 * 60)
    days = math.ceil(temp)
    return days

def abc_analysis(input):
    value, index = sort_with_index(input)
    label = perform_abc_analysis(value)
    output = unsort_with_index(label, index)
    return output

def scale_to_1(values):
    total_value = np.max(values)
    scaling = values / total_value
    return scaling

def perform_abc_analysis(values):
    # Calculate the total value and the cumulative percentage for each value
    total_value = np.sum(values)
    percentages = values / total_value
    cumulative_percentages = np.cumsum(percentages)

    # Classify the values into A, B, and C categories based on their cumulative percentage
    c_indices = np.where(cumulative_percentages <= 0.2)[0]
    b_indices = np.where((cumulative_percentages > 0.2) & (percentages <= 0.8))[0]
    a_indices = np.where(cumulative_percentages > 0.8)[0]

    # Create a new array with A, B, and C labels
    labels = np.full_like(values, "C", dtype=object)
    labels[b_indices] = "B"
    labels[a_indices] = "A"

    # Return the labels
    return labels

def sort_with_index(input):
    # Create an array with the original element positions
    original_index = np.arange(len(input))

    # Sort the input array in ascending order
    sorted_input = np.sort(input)
    
    # Update the original_index array based on the sorted input
    sorted_index = np.argsort(input)
    sorted_original_index = original_index[sorted_index]

    return sorted_input, sorted_original_index

def unsort_with_index(sorted_input, sorted_original_index):
    # Create an empty array to hold the unsorted input
    original_input = np.empty_like(sorted_input)

    # Use the sorted_original_index to restore the original order of the input
    for i, index in enumerate(sorted_original_index):
        original_input[index] = sorted_input[i]

    return original_input