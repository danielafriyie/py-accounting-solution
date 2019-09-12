import sqlite3 as sq
from inventory import inventory_data

i_data = inventory_data.InventoryDatabase(r"inventory_data.db")


class SalesData:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sales_data(id INTEGER PRIMARY KEY, date DATE, name TEXT,"
                            "address TEXT, loc TEXT, invoice_no TEXT,"
                            "customer_no TEXT, i_code TEXT, qty REAL, rte REAL, amt REAL)")
        self.connect.commit()

    def add_new(self, date, name, address, loc, invoice_no, customer_no, i_code, qty, rte, amt):
        self.cursor.execute("INSERT INTO sales_data VALUES (NULL, ?,?,?,?,?,?,?,?,?,?)",
                            (date, name, address, loc, invoice_no, customer_no, i_code, qty, rte, amt))
        self.connect.commit()
        i_data.update_inv_from_sales(i_code, qty, qty)

    def delete_with_invoice_no(self, invoice_no):
        self.cursor.execute("DELETE FROM sales_data WHERE invoice_no=?", (invoice_no,))
        self.connect.commit()

    def delete_with_id(self, id):
        self.cursor.execute("DELETE FROM sales_data WHERE id=?", (id,))
        self.connect.commit()

    def update(self, invoice_no, name, address, loc, customer_no, i_code, qty, rte, amt):
        self.cursor.execute("UPDATE sales_data SET name=?, address=?, loc=?, customer_no=?, i_code=?, qty=?, rte=?,"
                            "amt=? WHERE invoice_no=?",
                            (name, address, loc, customer_no, i_code, qty, rte, amt, invoice_no))
        self.connect.commit()

    def update_reflection(self, invoice_no):
        self.cursor.execute("SELECT qty FROM sales_data WHERE invoice_no=?", (invoice_no,))
        row = self.cursor.fetchall()
        return row

    def invoice_no_gen(self):
        self.cursor.execute("SELECT id FROM sales_data ORDER BY id DESC LIMIT 1")
        row = self.cursor.fetchall()
        return row

    def display_all(self):
        self.cursor.execute("SELECT id, i_code, date, invoice_no, customer_no, name, qty, rte, amt FROM sales_data")
        row = self.cursor.fetchall()
        return row

    def select_invoice_no(self):
        self.cursor.execute("SELECT invoice_no FROM sales_data")
        row = self.cursor.fetchall()
        return row

    def search_invoice(self, invoice_no):
        self.cursor.execute("SELECT * FROM sales_data WHERE invoice_no=?", (invoice_no,))
        row = self.cursor.fetchall()
        return row

    def invoice_no_check(self):
        self.cursor.execute("SELECT invoice_no FROM sales_data")
        row = self.cursor.fetchall()
        return row

    def track_deleted_data_by_id(self, id):
        self.cursor.execute("SELECT * FROM sales_data WHERE id=?", (id,))
        row = self.cursor.fetchall()
        return row

    def select_date(self, invoice_no):
        self.cursor.execute("SELECT date FROM sales_data WHERE invoice_no=?", (invoice_no,))
        row = self.cursor.fetchall()
        return row

    def get_qty_and_rte(self, invoice_no):
        self.cursor.execute("SELECT qty, rte FROM sales_data WHERE invoice_no=?", (invoice_no,))
        return self.cursor.fetchall()

    # ================= Sales Report Window ========================================
    def report(self, s_date, e_date):
        self.cursor.execute(
            "SELECT id, date, invoice_no, customer_no, i_code, amt FROM sales_data WHERE date BETWEEN ? AND ?",
            (s_date, e_date))
        return self.cursor.fetchall()

    def sum_amt(self, s_date, e_date):
        self.cursor.execute("SELECT SUM (amt) FROM sales_data WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def revenue(self, s_date, e_date):
        self.cursor.execute("SELECT invoice_no, i_code, amt FROM sales_data WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def close_database(self):
        self.connect.close()


class TrackSales:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS track_sales(id INTEGER PRIMARY KEY, date DATE,"
                            "i_code TEXT, inv_no TEXT, cus_no TEXT, name TEXT, qty REAL, rte REAL,"
                            "amt REAL, user_action TEXT)")
        self.connect.commit()

    def insert(self, date, i_code, inv_no, cus_no, name, qty, rte, amt, user_action):
        self.cursor.execute("INSERT INTO track_sales VALUES(NULL, ?,?,?,?,?,?,?,?,?)",
                            (date, i_code, inv_no, cus_no, name, qty, rte, amt, user_action))
        self.connect.commit()

    def display_all(self):
        self.cursor.execute("SELECT * FROM track_sales")
        row = self.cursor.fetchall()
        return row

    def cus_no_check(self):
        self.cursor.execute("SELECT cus_no FROM track_sales")
        row = self.cursor.fetchall()
        return row

    def inv_no_check(self):
        self.cursor.execute("SELECT inv_no FROM track_sales")
        row = self.cursor.fetchall()
        return row

    def item_code_check(self):
        self.cursor.execute("SELECT i_code FROM track_sales")
        row = self.cursor.fetchall()
        return row

    def search_with_cus_no(self, cus_no):
        self.cursor.execute("SELECT * FROM track_sales WHERE cus_no=?", (cus_no,))
        row = self.cursor.fetchall()
        return row

    def search_with_invoice_no(self, inv_no):
        self.cursor.execute("SELECT * FROM track_sales WHERE inv_no=?", (inv_no,))
        row = self.cursor.fetchall()
        return row

    def search_with_item_code(self, i_code):
        self.cursor.execute("SELECT * FROM track_sales WHERE i_code=?", (i_code,))
        row = self.cursor.fetchall()
        return row

    def close_database(self):
        self.connect.close()
