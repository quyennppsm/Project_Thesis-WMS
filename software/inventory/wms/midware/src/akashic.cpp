#include "funcs.h"

int main(){
    string file_path = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/";
    string file_akashic_order = "2019_order_5.csv";
    string file_akashic_carrier = "2019_carrier_5.csv";
    string file_db_product = "db_product.csv";
    string file_db_layout = "db_layout.csv";
    string file_log_akashic = "log_akashic.csv";

    string identification;
    struct_file order, carrier, record, statistic, log;

    clear_csv_file(file_path + file_akashic_order);
    clear_csv_file(file_path + file_akashic_carrier);
    //clear_csv_file(file_path + file_log_akashic);
    
    int buff, total = 75982216;
    int order_count = 0, carrier_count = 0;
    int maximus_item = 434;
    int maximus_coordinate = 18000;

    vector<string> order_identifications = read_csv_column(file_path + file_akashic_order, 1);
    vector<string> carrier_identifications = read_csv_column(file_path + file_akashic_carrier, 1);

    vector<string> product_identifications = read_csv_column(file_path + file_db_product, 1);
    vector<string> product_quantities = read_csv_column(file_path + file_db_product, 2);

    vector<string> layout_coordinates = read_csv_column(file_path + file_db_layout, 1);
    
    order.name.assign(file_path + file_akashic_order);
    carrier.name.assign(file_path + file_akashic_carrier);
    log.name.assign(file_path + file_log_akashic);

    order.action.open(order.name,ios::out);
    carrier.action.open(carrier.name,ios::out);
    log.action.open(log.name,ios::app);

    log.action
        << "akashic record "
        << file_akashic_order << ", "
        << file_akashic_carrier << ", "
        <<  get_current_time() << ", ";
    order.action
        << "id, identification, timestamp, despatch";
    carrier.action
        << "id, identification, receive, despatch, timestamp, timedespatch, product, coordinate, order";

    int rand_carrier_total;
    int rand_item;
    long long milestone1 = get_timestamp(1, 1, 2019);
    long long milestone2 = get_timestamp(31, 12, 2019);
    buff = 0;
    while(buff < total){
        order_count++;
        string order_new_id = generate_unique_string(order_identifications);
        long long timestamp = random_long_long(milestone1, milestone2);
        long long destpach = random_long_long(timestamp, milestone2);
        order.action
            << endl
            << order_count << ", "
            << order_new_id << ", "
            << get_time_string(timestamp) << ", "
            << get_time_string(destpach);
        
        int rand_order_total = random_int(5, 25);
        for (int i = 1; i <= rand_order_total; i++){
            rand_carrier_total = random_int(1, 17);
            rand_item = random_int(0, maximus_item-1);
            for (int j = 1; j <= rand_carrier_total; j++){
                string carrier_new_id = generate_unique_string(carrier_identifications);
                int rand_coordinate = random_int(0, maximus_coordinate-1);
                carrier_count++;
                buff = buff + stoi(product_quantities[rand_item]);
                carrier.action
                    << endl
                    << carrier_count << ", "
                    << carrier_new_id << ", "
                    << "1, 1, "
                    << get_time_string(timestamp) << ", "
                    << get_time_string(destpach) << ", "
                    << product_identifications[rand_item] << ", "
                    << layout_coordinates[rand_coordinate] << ", "
                    << order_new_id;
                cout
                    << endl
                    << carrier_count << ", "
                    << buff << ", "
                    << total - buff << ", "
                    << product_identifications[rand_item];
                if (buff > total){
                    break;
                }
            }
        }
    } 

    log.action
        << carrier_count << ", "
        << buff << ", "
        << get_current_time() << endl;

    order.action.close();
    carrier.action.close();
    record.action.close();
    statistic.action.close();
    log.action.close();

    return 0;
}