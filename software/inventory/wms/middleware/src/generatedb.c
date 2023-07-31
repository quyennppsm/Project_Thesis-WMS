#include "funcs.c"

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <database_name>\n", argv[0]);
        return 1;
    }

    const char *parent_dir_path = "C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/middleware/db/";
    char *db_file_path = malloc(strlen(parent_dir_path) + strlen(argv[1]) + 1);
    sprintf(db_file_path, "%s%s", parent_dir_path, argv[1]);

    sqlite3 *db;
    char *err_msg = 0;
    int rc;

    rc = sqlite3_open(db_file_path, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Error: cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        free(db_file_path);
        return 1;
    }

    sqlite3_close(db);
    free(db_file_path);

    return 0;
}