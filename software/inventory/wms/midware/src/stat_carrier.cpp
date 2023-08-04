#include "nfuncs.h"

int main() {
    string file_path = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/dataset/";
    string file_proc_carrier = file_path + "proc_2019_carrier_0.csv";
    string file_stat_product = file_path + "stat_2019_product_0.csv";
    string file_abc_product = file_path + "abc_2019_product_0.csv";
    string db_product = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/db_product.csv";

    ofstream file(file_stat_product);
    ofstream abc(file_abc_product);
    file
        << "id, product, total_despatched, total_age, total_cost, total_wage, demand, flow, total_order";
    abc
        << "id, product, total_despatched, total_age, total_cost, total_wage, demand, flow, total_order";
    cout
        << "id, product, total_despatched, total_age, total_cost, total_wage, demand, flow, total_order";

    vector<string> db_identification = read_csv_column(db_product, 1);
    vector<string> db_cost = read_csv_column(db_product, 3);
    vector<string> db_wage = read_csv_column(db_product, 6);

    vector<string> all_age = read_csv_column(file_proc_carrier, 4);
    vector<string> all_product = read_csv_column(file_proc_carrier, 5);
    vector<string> all_order = read_csv_column(file_proc_carrier, 7);

    vector<string> unq_product = unique_list(all_product);
    vector<string> unq_order;
    vector<long long> t_age, c_order, t_cost, t_wage;
    t_age.resize(unq_product.size(), 0);    
    c_order.resize(unq_product.size(), 0);
    t_cost.resize(unq_product.size(), 0);    
    t_wage.resize(unq_product.size(), 0);
    int count, pos;
    long long asc_des = 0;
    long long asc_age = 0;
    long long asc_cos = 0;
    long long asc_wag = 0;
    double asc_dem = 0;
    double asc_flo = 0;
    long long asc_ord = 0;

    for (int i = 0; i < unq_product.size(); i++){
        unq_order.clear();
        count = 0;
        pos = 0;
        t_age[i] = 0;
        t_cost[i] = 0;
        t_wage[i] = 0;

        for (int j = 0; j < all_product.size(); j++){
            if (unq_product[i] == all_product[j]){
                t_age[i] = t_age[i] + stoll(all_age[j]);
                insert_value(unq_order, all_order[j], count);
                count++;
            }
        }
        for (int j = 0; j < db_identification.size(); j++){
            if (unq_product[i] == db_identification[j]){
                pos = j;
                break;
            }
        }
        c_order[i] = count_unique(unq_order);
        t_cost[i] = stoll(db_cost[pos]) * count;
        t_wage[i] = stoll(db_wage[pos]) * count;
        file
            << endl
            << i+1 << ", "
            << unq_product[i] << ", "
            << count << ", "
            << t_age[i] << ", "
            << t_cost[i] << ", "
            << t_wage[i] << ", "
            << longlong_divide(count, 365) << ", "
            << longlong_divide(count, c_order[i]) << ", "
            << c_order[i];
        asc_des = asc_des + count;
        asc_age = asc_age + t_age[i];
        asc_cos = asc_cos + t_cost[i];
        asc_wag = asc_wag + t_wage[i];
        asc_dem = asc_dem + stod(longlong_divide(count, 365));
        asc_flo = asc_flo + stod(longlong_divide(count, c_order[i]));
        asc_ord = asc_ord + c_order[i];
        
    }
    for (int i = 0; i < unq_product.size(); i++){
        abc
            << endl
            << i+1 << ", "
            << unq_product[i] << ", "
            << longlong_divide(count, asc_des) << ", "
            << longlong_divide(t_age[i], asc_age) << ", "
            << longlong_divide(t_cost[i], asc_cos) << ", "
            << longlong_divide(t_wage[i], asc_wag) << ", "
            << stod(longlong_divide(count, 365)) / asc_dem << ", "
            << stod(longlong_divide(count, c_order[i])) / asc_flo << ", "
            << longlong_divide(c_order[i], asc_ord);
        cout
            << endl
            << i+1 << ", "
            << unq_product[i] << ", "
            << longlong_divide(count, asc_des) << ", "
            << longlong_divide(t_age[i], asc_age) << ", "
            << longlong_divide(t_cost[i], asc_cos) << ", "
            << longlong_divide(t_wage[i], asc_wag) << ", "
            << stod(longlong_divide(count, 365)) / asc_dem << ", "
            << stod(longlong_divide(count, c_order[i])) / asc_flo << ", "
            << longlong_divide(c_order[i], asc_ord);
    }

    return 0;
}