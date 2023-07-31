#include "libs.h"

string addIntToString(int num, const string& str) {
    return str + to_string(num);
}

void clear_csv_file(
    string file_path
    ) 
{
    ofstream file(file_path, ios::trunc);
    file.close();
}

vector<string> read_csv_column(string filename, int col_index) {
    vector<string> column_values;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: could not open file " << filename << endl;
        return column_values;
    }
    string line, value;
    // Read the header line and discard it
    getline(file, line);
    while (getline(file, line)) {
        stringstream ss(line);
        for (int i = 0; i < col_index; i++) {
            getline(ss, value, ',');
        }
        getline(ss, value, ',');
        column_values.push_back(value);
    }
    file.close();
    return column_values;
}

string generate_unique_string(const vector<string>& existing_strings) {
    static const char alphanum[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";
    static const int alphanum_size = sizeof(alphanum) - 1;
    static random_device rd;
    static mt19937 gen(rd());
    static uniform_int_distribution<> dis(0, alphanum_size - 1);
    
    string new_string;
    while (new_string.length() < 20) {
        new_string += alphanum[dis(gen)];
    }
    
    auto it = find(existing_strings.begin(), existing_strings.end(), new_string);
    if (it == existing_strings.end()) {
        return new_string;
    } else {
        return generate_unique_string(existing_strings);
    }
}

bool has_duplicates(const vector<string>& strings) {
    unordered_set<string> string_set;
    for (const string& s : strings) {
        if (string_set.count(s) > 0) {
            return true;
        }
        string_set.insert(s);
    }
    return false;
}

long long get_timestamp(int day, int month, int year) {
    tm timeinfo = {};
    timeinfo.tm_year = year - 1900;
    timeinfo.tm_mon = month - 1;
    timeinfo.tm_mday = day;
    time_t time = mktime(&timeinfo);
    if (time == -1) {
        cerr << "Error: invalid date" << endl;
        return -1;
    }
    return time * 1000LL;
}

long long generate_timestamp(long long milestone1, long long milestone2) {
    if (milestone1 >= milestone2) {
        cerr << "Error: milestone1 should be smaller than milestone2" << endl;
        return -1;
    }
    long long duration = milestone2 - milestone1;
    auto now = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
    long long timestamp = milestone1 + (now.count() % duration);
    return timestamp;
}

string get_time_string(long long timestamp) {
    auto time = system_clock::time_point(milliseconds(timestamp));
    time_t t = system_clock::to_time_t(time);
    char buffer[80];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", localtime(&t));
    return string(buffer);
}

int get_day_of_year(int day, int month, int year) {
    int days_in_month[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int day_of_year = day;
    for (int i = 0; i < month - 1; ++i) {
        day_of_year += days_in_month[i];
        if (i == 1 && ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)) {
            day_of_year += 1;
        }
    }
    return day_of_year;
}