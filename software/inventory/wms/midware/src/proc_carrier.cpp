#include "funcs.h"

int main() {
    string file_path = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/dataset/";
    string file_akashic_carrier = "2019_carrier_0.csv";
    string file_proc_carrier = "proc_2019_carrier_0.csv";

    string akashic_carrier = file_path + file_akashic_carrier;
    string proc_carrier = file_path + file_proc_carrier;

    cout
        << "Proc start: [" << get_current_time() << "]: "
        << akashic_carrier << endl
        << proc_carrier << endl;

    ofstream file(proc_carrier);
    file
        << "id, identification, timestamp, timedespatch, age, product, coordinate, order";

    vector<string> id = read_csv_column(akashic_carrier, 0);
    vector<string> identification = read_csv_column(akashic_carrier, 1);
    vector<string> timestamp = read_csv_column(akashic_carrier, 4);
    vector<string> timedespatch = read_csv_column(akashic_carrier, 5);
    vector<string> product = read_csv_column(akashic_carrier, 6);
    vector<string> coordinate = read_csv_column(akashic_carrier, 7);
    vector<string> order = read_csv_column(akashic_carrier, 8);

    cout
        << endl
        << "File read: [" << get_current_time() << "]: "
        << akashic_carrier << endl;

    vector<vector<string>::iterator> timestamp_iters;
    for (auto it = timestamp.begin(); it != timestamp.end(); ++it) {
        timestamp_iters.push_back(it);
    }
    sort(timestamp_iters.begin(), timestamp_iters.end(),
        [&](auto a, auto b) { return *a > *b; });
    vector<string> ti_sorted_id;
    vector<string> ti_sorted_identification;
    vector<string> ti_sorted_timestamp;
    vector<string> ti_sorted_timedespatch;
    vector<string> ti_sorted_product;
    vector<string> ti_sorted_coordinate;
    vector<string> ti_sorted_order;
    for (auto it : timestamp_iters) {
        int index = distance(timestamp.begin(), it);
        ti_sorted_id.push_back(id[index]);
        ti_sorted_identification.push_back(identification[index]);
        ti_sorted_timestamp.push_back(timestamp[index]);
        ti_sorted_timedespatch.push_back(timedespatch[index]);
        ti_sorted_product.push_back(product[index]);
        ti_sorted_coordinate.push_back(coordinate[index]);
        ti_sorted_order.push_back(order[index]);
    }
    
    cout
        << endl
        << "File sort :[" << get_current_time() << "]: "
        << proc_carrier << endl;

    for (int i = 0; i < ti_sorted_id.size(); ++i) {
        file   
            << endl
            << i+1 << ", " 
            << ti_sorted_identification[i] << ", "
            << reverse_timestamp(ti_sorted_timestamp[i]) << ", " 
            << reverse_timestamp(ti_sorted_timedespatch[i]) << ", "
            << reverse_timestamp(ti_sorted_timedespatch[i]) - reverse_timestamp(ti_sorted_timestamp[i]) << ", "
            << ti_sorted_product[i] << ", "
            << ti_sorted_coordinate[i] << ", "
            << ti_sorted_order[i];
    }
    
    cout
        << endl
        << "Proc done: [" << get_current_time() << "]: END";

    return 0;
}