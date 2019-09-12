import sqlite3 as sq
from inventory import inventory_data

i_data = inventory_data.InventoryDatabase(r"inventory_data.db")


class PurchasesData:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS purchases_data(id INTEGER PRIMARY KEY, date DATE, name TEXT,"
                            "address TEXT, loc TEXT, invoice_no TEXT,"
                            "account_no TEXT, i_code TEXT, qty REAL, rte REAL, amt REAL)")
        self.connect.commit()

    def add_new(self, date, name, address, loc, invoice_no, account_no, i_code, qty, rte, amt):
        self.cursor.execute("INSERT INTO purchases_data VALUES (NULL, ?,?,?,?,?,?,?,?,?,?)",
                            (date, name, address, loc, invoice_no, account_no, i_code, qty, rte, amt))
        self.connect.commit()
        # i_data.update_inv_from_purchases(i_code, qty, qty)

    def delete_with_invoice_no(self, invoice_no):
        self.cursor.execute("DELETE FROM purchases_data WHERE invoice_no=?", (invoice_no,))
        self.connect.commit()

    def delete_with_id(self, id):
        self.cursor.execute("DELETE FROM purchases_data WHERE id=?", (id,))
        self.connect.commit()

    def update(self, invoice_no, name, address, loc, account_no, i_code, qty, rte, amt):
        self.cursor.execute("UPDATE purchases_data SET name=?, address=?, loc=?, account_no=?, i_code=?, qty=?, rte=?,"
                            "amt=? WHERE invoice_no=?",
                            (name, address, loc, account_no, i_code, qty, rte, amt, invoice_no))
        self.connect.commit()

    def invoice_no_gen(self):
        self.cursor.execute("SELECT id FROM purchases_data ORDER BY id DESC LIMIT 1")
        row = self.cursor.fetchall()
        return row

    def display_all(self):
        self.cursor.execute("SELECT id, i_code, date, invoice_no, account_no, name, qty, rte, amt FROM purchases_data")
        row = self.cursor.fetchall()
        return row

    def select_invoice_no(self):
        self.cursor.execute("SELECT invoice_no FROM purchases_data")
        row = self.cursor.fetchall()
        return row

    def search_invoice(self, invoice_no):
        self.cursor.execute("SELECT * FROM purchases_data WHERE invoice_no=?", (invoice_no,))
        row = self.cursor.fetchall()
        return row

    def invoice_no_check(self):
        self.cursor.execute("SELECT invoice_no FROM purchases_data")
        row = self.cursor.fetchall()
        return row

    def track_deleted_data_by_id(self, id):
        self.cursor.execute("SELECT * FROM purchases_data WHERE id=?", (id,))
        row = self.cursor.fetchall()
        return row

    def update_reflection(self, invoice_no):
        self.cursor.execute("SELECT qty FROM purchases_data WHERE invoice_no=?", (invoice_no,))
        row = self.cursor.fetchall()
        return row

    def get_qty_and_rte(self, invoice_no):
        self.cursor.execute("SELECT qty, rte FROM purchases_data WHERE invoice_no=?", (invoice_no,))
        return self.cursor.fetchall()

    # ================= Purchase Report Window ========================================
    def report(self, s_date, e_date):
        self.cursor.execute(
            "SELECT id, date, invoice_no, account_no, i_code, amt FROM purchases_data WHERE date BETWEEN ? AND ?",
            (s_date, e_date))
        return self.cursor.fetchall()

    def sum_amt(self, s_date, e_date):
        self.cursor.execute("SELECT SUM (amt) FROM purchases_data WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def close_database(self):
        self.connect.close()


class TrackPurchases:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS track_purchase(id INTEGER PRIMARY KEY, date DATE,"
                            "i_code TEXT, inv_no TEXT, account_no TEXT, name TEXT, qty REAL, rte REAL,"
                            "amt REAL, user_action TEXT)")
        self.connect.commit()

    def insert(self, date, i_code, inv_no, account_no, name, qty, rte, amt, user_action):
        self.cursor.execute("INSERT INTO track_purchase VALUES(NULL, ?,?,?,?,?,?,?,?,?)",
                            (date, i_code, inv_no, account_no, name, qty, rte, amt, user_action))
        self.connect.commit()

    def display_all(self):
        self.cursor.execute("SELECT * FROM track_purchase")
        row = self.cursor.fetchall()
        return row

    def account_no_check(self):
        self.cursor.execute("SELECT account_no FROM track_purchase")
        row = self.cursor.fetchall()
        return row

    def inv_no_check(self):
        self.cursor.execute("SELECT inv_no FROM track_purchase")
        row = self.cursor.fetchall()
        return row

    def item_code_check(self):
        self.cursor.execute("SELECT i_code FROM track_purchase")
        row = self.cursor.fetchall()
        return row

    def search_with_account_no(self, account_no):
        self.cursor.execute("SELECT * FROM track_purchase WHERE account_no=?", (account_no,))
        row = self.cursor.fetchall()
        return row

    def search_with_invoice_no(self, inv_no):
        self.cursor.execute("SELECT * FROM track_purchase WHERE inv_no=?", (inv_no,))
        row = self.cursor.fetchall()
        return row

    def search_with_item_code(self, i_code):
        self.cursor.execute("SELECT * FROM track_purchase WHERE i_code=?", (i_code,))
        row = self.cursor.fetchall()
        return row

    def close_database(self):
        self.connect.close()
