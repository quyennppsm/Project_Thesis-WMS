#include "funcs.h"

int main(){
    string file_path = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/";
    string file_name = "layout.csv";
    string file = file_path + file_name;

    clear_csv_file(file);
    
    int id = 0;
    string identification;
    struct_file layout;

    layout.name.assign(file);
    layout.action.open(layout.name,ios::out);

    layout.action
        << "id, identification, floor, section, location, shelf, column, row, emc";

    for (int a = 1; a <= c_floor; a++){
        for (int b = 1; b <= c_section; b++){
            for (int c = 1; c <= c_location; c++){
                for (int d = 1; d <= c_shelf; d++){
                    for (int e = 1; e <= c_column; e++){
                        for (int f = 1; f <= c_row; f++){
                            id++;
                            identification = "";
                            identification = addIntToString(a,identification);
                            identification = addIntToString(b,identification);
                            identification = addIntToString(c,identification);
                            identification = addIntToString(d,identification);
                            identification = addIntToString(e,identification);
                            identification = addIntToString(f,identification);
                            layout.action
                                << endl 
                                << id << ", "
                                << identification << ", "
                                << a << ", "
                                << b << ", "
                                << c << ", "
                                << d << ", "
                                << e << ", "
                                << f << ", 0";
                        }
                    }
                }
            }
            if (b == 8){
                for (int c = 0; c < 4; c++){
                    string alpha_location[4] = {"A", "B", "C", "D"};
                    for (int d = 1; d <= c_shelf; d++){
                        for (int e = 1; e <= c_column; e++){
                            for (int f = 1; f <= c_row; f++){
                                id++;
                                identification = "";
                                identification = addIntToString(a,identification);
                                identification = addIntToString(b,identification);
                                identification = identification + alpha_location[c];
                                identification = addIntToString(d,identification);
                                identification = addIntToString(e,identification);
                                identification = addIntToString(f,identification);
                                layout.action
                                    << endl 
                                    << id << ", "
                                    << identification << ", "
                                    << a << ", "
                                    << b << ", "
                                    << alpha_location[c] << ", "
                                    << d << ", "
                                    << e << ", "
                                    << f << ", 1";
                            }
                        }
                    }
                }
            }
        }
    }

    layout.action.close();

    return 0;
}