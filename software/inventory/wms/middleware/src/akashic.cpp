#include "funcs.h"

int main(){
    string file_path = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/";
    string file_order = "order.csv";
    string file_carrier = "carrier.csv";
    string file_record = "record.csv";
    string file_statistic = "statistic.csv";
    string file_product = "product.csv";
    string file_layout = "layout.csv";
    string file_slot = "slot.csv";

    clear_csv_file(file_path + file_order);
    clear_csv_file(file_path + file_carrier);
    clear_csv_file(file_path + file_record);
    clear_csv_file(file_path + file_statistic);
    
    int count = 0;
    string identification;
    struct_file order, carrier, record, statistic;

    order.name.assign(file_path + file_order);
    carrier.name.assign(file_path + file_carrier);
    record.name.assign(file_path + file_record);
    statistic.name.assign(file_path + file_statistic);

    order.action.open(order.name,ios::out);
    carrier.action.open(carrier.name,ios::out);
    record.action.open(record.name,ios::out);
    statistic.action.open(statistic.name,ios::out);

    order.action
        << "id, identification, timestamp, despatch";
    carrier.action
        << "id, identification, receive, despatch, timestamp, coordinate, product, order";
    record.action
        << "id, identification, p_quantity, p_cost, p_wage, p_emc, c_total, c_reserved, c_available, t_order, t_day, t_despatch, r_frequency, r_flow, r_demand, s_value, s_percentage, s_assign";
    statistic.action
        << "id, identification, year, a_order, a_day, a_despatch, a_value";

    vector<string> order_identifications = read_csv_column(file_path + file_order, 1);
    long long milestone1 = get_timestamp(1, 1, 2019);
    long long milestone2 = get_timestamp(31, 12, 2019);
    for (int i = 0; i < 10000; i++){
        string new_identification = generate_unique_string(order_identifications);
        long long timestamp = generate_timestamp(milestone1, milestone2);
        long long destpach = generate_timestamp(timestamp, milestone2);
        order.action
            << endl
            << i+1 << ", "
            << new_identification << ", "
            << get_time_string(timestamp) << ", "
            << get_time_string(destpach);
    }

    order_identifications.clear();

    order.action.close();
    carrier.action.close();
    record.action.close();
    statistic.action.close();

    

    return 0;
}