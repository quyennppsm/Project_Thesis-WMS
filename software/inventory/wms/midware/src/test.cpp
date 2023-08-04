#include <bits/stdc++.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <random>
#include <string>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <unordered_map>

using namespace std;

struct struct_file{
    fstream action;
    string name;
};

// Function to calculate the area of a rectangle
double calc_area(double length, double width) {
    return length * width;
}

int main() {
    // Test the calc_area function
    double length = 5.0;
    double width = 3.0;
    double expected_area = 15.0;
    double actual_area = calc_area(length, width);

    // Check if the actual area matches the expected area
    if (expected_area == actual_area) {
        cout << "Test passed: calc_area(" << length << ", " << width << ") = " << actual_area << endl;
    } else {
        cout << "Test failed: calc_area(" << length << ", " << width << ") = " << actual_area << ", expected " << expected_area << endl;
    }

    string file_test = "test.csv";

    struct_file test;

    test.name.assign(file_test);
    test.action.open(test.name, ios::app);

    return 0;
}