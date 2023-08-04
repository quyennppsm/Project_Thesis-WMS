#include "funcs.h"

int main(){
    string file_path = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/";
    string file_test = "test.csv";

    struct_file test;

    test.name.assign(file_path + file_test);
    test.action.open(test.name, ios::app);

    long long milestone1 = get_timestamp(1, 1, 2019);
    long long milestone2 = get_timestamp(31, 12, 2019);

    for (int i = 1; i <= 20; i++){
        long long timestamp = random_long_long(milestone1, milestone2);
        long long destpach = random_long_long(timestamp, milestone2);

        test.action
            << i << ", "
            << milestone1 << ", "
            << get_time_string(milestone1) << ", "
            << timestamp << ", "
            << get_time_string(timestamp) << ", "
            << milestone2 << ", "
            << get_time_string(milestone2) << ", "
            << destpach << ", "
            << get_time_string(destpach) << ", "
            << endl;
    }

    test.action.close();

    return 0;
}