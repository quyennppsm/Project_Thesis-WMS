#include "funcs.h"

int main() {
    string file_name = "input.csv";
    string output_filename = "output.csv";

    vector<string> id = read_csv_column(file_name, 0);
    vector<string> identification = read_csv_column(file_name, 1);
    vector<string> timestamp = read_csv_column(file_name, 2);
    vector<string> despatch = read_csv_column(file_name, 3);

    // Create a vector of iterators to the despatch vector
    std::vector<std::vector<std::string>::iterator> despatch_iters;
    for (auto it = despatch.begin(); it != despatch.end(); ++it) {
        despatch_iters.push_back(it);
    }
    
    // Sort the iterators based on the despatch vector
    sort(despatch_iters.begin(), despatch_iters.end(),
              [&](auto a, auto b) { return *a > *b; });

    // Apply the same order to the other vectors
    vector<string> de_sorted_id;
    vector<string> de_sorted_identification;
    vector<string> de_sorted_timestamp;
    vector<string> de_sorted_despatch;
    for (auto it : despatch_iters) {
        int index = distance(despatch.begin(), it);
        de_sorted_id.push_back(id[index]);
        de_sorted_identification.push_back(identification[index]);
        de_sorted_timestamp.push_back(timestamp[index]);
        de_sorted_despatch.push_back(despatch[index]);
    }

    // Create a vector of iterators to the timestamp vector
    std::vector<std::vector<std::string>::iterator> timestamp_iters;
    for (auto it = timestamp.begin(); it != timestamp.end(); ++it) {
        timestamp_iters.push_back(it);
    }
    
    // Sort the iterators based on the timestamp vector
    sort(timestamp_iters.begin(), timestamp_iters.end(),
              [&](auto a, auto b) { return *a > *b; });

    // Apply the same order to the other vectors
    vector<string> ti_sorted_id;
    vector<string> ti_sorted_identification;
    vector<string> ti_sorted_timestamp;
    vector<string> ti_sorted_despatch;
    for (auto it : timestamp_iters) {
        int index = distance(timestamp.begin(), it);
        ti_sorted_id.push_back(id[index]);
        ti_sorted_identification.push_back(identification[index]);
        ti_sorted_timestamp.push_back(timestamp[index]);
        ti_sorted_despatch.push_back(despatch[index]);
    }

    // Write the sorted vectors to a CSV file
    ofstream output_file(output_filename);
    output_file 
        << "id, identification, timestamp, timedespatch, t_age, age";
    for (int i = 0; i < ti_sorted_id.size(); ++i) {
        output_file 
            << endl
            << i << ", " 
            << ti_sorted_identification[i] << ", "
            << reverse_timestamp(ti_sorted_timestamp[i]) << ", " 
            << reverse_timestamp(ti_sorted_despatch[i]) << ", "
            << reverse_timestamp(ti_sorted_despatch[i]) - reverse_timestamp(ti_sorted_timestamp[i]) << ", "
            << format_duration(create_duration(reverse_timestamp(ti_sorted_despatch[i]) - reverse_timestamp(ti_sorted_timestamp[i])));
    }

    return 0;
}