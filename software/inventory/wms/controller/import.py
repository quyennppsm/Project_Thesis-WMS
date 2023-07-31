import csv
import sqlite3

def import_data():
    conn = sqlite3.connect('C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/db.sqlite3')
    c = conn.cursor()

#    c.execute('DELETE FROM controller_slot;')

    with open('C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/product.csv') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            # Check if a row with the same identification already exists in the Product table
            c.execute("SELECT * FROM controller_product WHERE identification=?", (row[1],))
            result = c.fetchone()

            if result:
                # If a row with the same identification exists, update its values
                c.execute("""
                    UPDATE controller_product
                    SET quantity=?, cost=?, price=?, profit=?, wage=?, description=?
                    WHERE identification=?
                """, (row[2], row[3], row[4], row[5], row[6], row[7], row[1]))
            else:
                # Otherwise, insert a new row with the data from the CSV row
                c.execute("""
                    INSERT INTO controller_product (identification, quantity, cost, price, profit, wage, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, row[1:])

    with open('C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/layout.csv') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            # Check if a row with the same identification already exists in the Product table
            c.execute("SELECT * FROM controller_product WHERE identification=?", (row[1],))
            result = c.fetchone()

            if result:
                # If a row with the same identification exists, update its values
                c.execute("""
                    UPDATE controller_layout
                    SET floor=?, section=?, location=?, shelf=?, column=?, row=?, emc=?
                    WHERE identification=?
                """, (row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[1]))
            else:
                # Otherwise, insert a new row with the data from the CSV row
                c.execute("""
                    INSERT INTO controller_layout (identification, floor, section, location, shelf, column, row, emc)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, row[1:])
   
    with open('C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/csv/slot.csv') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            # Check if a row with the same identification already exists in the Product table
            c.execute("SELECT * FROM controller_slot WHERE identification=?", (row[1],))
            result = c.fetchone()

            if result:
                # If a row with the same identification exists, update its values
                c.execute("""
                    UPDATE controller_slot
                    SET prefer=?, empty=?, reserved=?, age=?, product=?, carrier=?, order=? 
                    WHERE identification=?
                """, (row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[1]))
            else:
                # Otherwise, insert a new row with the data from the CSV row
                c.execute("""
                    INSERT INTO controller_slot (identification, prefer, empty, reserved, age, product, carrier, "order")
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, row[1:])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    import_data()