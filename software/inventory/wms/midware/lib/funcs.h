#include "libs.h"

string addIntToString(int num, const string& str) {
    return str + to_string(num);
}

void clear_csv_file(string file_path) {
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

string get_time_string(long long timestamp) {
    auto time = system_clock::time_point(milliseconds(timestamp));
    time_t t = system_clock::to_time_t(time);
    char buffer[80];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", localtime(&t));
    return string(buffer);
}

long long reverse_timestamp(const std::string& time_string) {
    std::tm tm = {};
    std::istringstream ss(time_string);
    ss >> std::get_time(&tm, "%Y-%m-%d %H:%M:%S");
    auto time_point = std::chrono::system_clock::from_time_t(std::mktime(&tm));
    return std::chrono::duration_cast<std::chrono::milliseconds>(time_point.time_since_epoch()).count();
}

string format_duration(std::chrono::milliseconds duration) {
    // Convert the duration to hours, minutes, and seconds
    std::chrono::hours hours = std::chrono::duration_cast<std::chrono::hours>(duration);
    duration -= hours;
    std::chrono::minutes minutes = std::chrono::duration_cast<std::chrono::minutes>(duration);
    duration -= minutes;
    std::chrono::seconds seconds = std::chrono::duration_cast<std::chrono::seconds>(duration);

    // Format the duration as a string
    std::ostringstream oss;
    oss << std::setfill('0') << std::setw(2) << hours.count() << ":"
        << std::setfill('0') << std::setw(2) << minutes.count() << ":"
        << std::setfill('0') << std::setw(2) << seconds.count();
    return oss.str();
}

std::chrono::milliseconds create_duration(long long duration_ms) {
    return std::chrono::milliseconds(duration_ms);
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

int random_int(int a, int b) {
    static std::random_device rd;  // obtain a random number from hardware
    static std::mt19937 gen(rd());  // seed the generator only once
    std::uniform_int_distribution<> distr(a, b);  // define the range

    return distr(gen);  // generate the random number
}

long long random_long_long(long long a, long long b) {
    static std::random_device rd;
    static std::mt19937_64 gen(rd());
    std::uniform_int_distribution<long long> distr(a, b);

    return distr(gen);
}

int count_csv_lines(const std::string& filename) {
    std::ifstream file(filename);
    int line_count = 0;
    std::string line;
    while (std::getline(file, line)) {
        ++line_count;
    }
    return line_count;
}

int increment_number_in_string(const std::string& str) {
    int num = std::atoi(str.c_str()); // convert string to integer
    num++; // increment the integer
    return num; // return the incremented integer
}

string get_current_time() {
    // Get the current system time
    auto now = std::chrono::system_clock::now();
    std::time_t time = std::chrono::system_clock::to_time_t(now);

    // Convert the time to a string
    std::stringstream ss;
    ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
    std::string time_str = ss.str();

    return time_str;
}