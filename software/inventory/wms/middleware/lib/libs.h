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

using namespace std;
using namespace chrono;

// Constants
const int c_floor = 3;
const int c_section = 8;
const int c_location = 7;
const int c_shelf = 4;
const int c_column = 5;
const int c_row = 5;

// structure to process file
struct struct_file{
    fstream action;
    string name;
};