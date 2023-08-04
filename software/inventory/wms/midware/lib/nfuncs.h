#include "funcs.h"

int count_unique_days(const std::vector<std::string>& str_vec) {
    std::set<std::string> unique_days;
    for (const auto& elem : str_vec) {
        // Extract the day part of the timestamp
        std::string day = elem.substr(0, 10);
        unique_days.insert(day);
    }
    return unique_days.size();
}

std::string longlong_divide(long long dividend, long long divisor) {
    double quotient = static_cast<double>(dividend) / static_cast<double>(divisor);
    std::stringstream ss;
    ss << std::fixed << std::setprecision(8) << quotient;
    return ss.str();
}

int count_unique(const std::vector<std::string>& str_vec) {
    std::set<std::string> unique_set;
    for (const auto& elem : str_vec) {
        unique_set.insert(elem);
    }
    return unique_set.size();
}

void insert_value(std::vector<std::string>& str_vec, const std::string& value, int pos) {
    str_vec.insert(str_vec.begin() + pos, value);
}

std::vector<int> str_to_int(const std::vector<std::string>& str_vec) {
    std::vector<int> int_vec(str_vec.size());

    for (int i = 0; i < str_vec.size(); i++) {
        int_vec[i] = std::stoi(str_vec[i]);
    }

    return int_vec;
}

std::vector<std::string> unique_list(const std::vector<std::string>& input_list) {
    // Create a new vector to hold the unique elements
    std::vector<std::string> unique_elements;

    // Copy the input vector to a temporary vector
    std::vector<std::string> temp_list(input_list);

    // Sort the temporary vector
    std::sort(temp_list.begin(), temp_list.end());

    // Remove duplicates from the temporary vector
    auto last = std::unique(temp_list.begin(), temp_list.end());
    temp_list.erase(last, temp_list.end());

    // Copy the unique elements to the output vector
    for (const auto& elem : temp_list) {
        unique_elements.push_back(elem);
    }

    return unique_elements;
}