import sqlite3 as sq


class InventoryDatabase:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS inventory(item_no INTEGER PRIMARY KEY, date DATE, i_code TEXT, descp TEXT, "
            "unit TEXT, rate REAL, qty REAL, amount REAL, rmks TEXT)")
        self.connect.commit()

    def save_btn(self, date, i_code, descp, unit, rate, qty, amount, rmks):
        self.cursor.execute("INSERT INTO inventory VALUES(NULL,?,?,?,?,?,?,?,?)",
                            (date, i_code, descp, unit, rate, qty, amount, rmks))
        self.connect.commit()

    def delete_btn(self, item_no):
        self.cursor.execute("DELETE FROM inventory WHERE item_no=?", (item_no,))
        self.connect.commit()

    def edit_btn(self, item_no):
        self.cursor.execute("SELECT * FROM inventory WHERE item_no=?", (item_no,))
        row = self.cursor.fetchall()
        return row

    def update_btn(self, item_no, date, i_code, descp, unit, rate, qty, amount, rmks):
        self.cursor.execute("UPDATE inventory SET date=?, i_code=?, descp=?, unit=?, rate=?, qty=?, amount=?, rmks=? "
                            "WHERE item_no=?", (date, i_code, descp, unit, rate, qty, amount, rmks, item_no))
        self.connect.commit()

    def search_with_code(self):
        self.cursor.execute("SELECT i_code FROM inventory")
        row = self.cursor.fetchall()
        return row

    def display_data(self):
        self.cursor.execute("SELECT * FROM inventory")
        row = self.cursor.fetchall()
        return row

    def display_item_code(self):
        self.cursor.execute("SELECT i_code FROM inventory ORDER BY i_code ASC")
        row = self.cursor.fetchall()
        return row

    def get_selected_row(self, i_code):
        self.cursor.execute("SELECT * FROM inventory WHERE i_code=?", (i_code,))
        row = self.cursor.fetchall()
        return row

    def item_no_select(self):
        self.cursor.execute("SELECT item_no FROM inventory ORDER BY item_no DESC LIMIT 1")
        row = self.cursor.fetchall()
        return row

    def get_des(self, i_code):
        self.cursor.execute("SELECT descp FROM inventory WHERE i_code=?", (i_code,))
        return self.cursor.fetchall()

    # =============== SALES DATA ===========================================

    def update_inv_from_sales(self, i_code, sales_qty, sales_qty2):
        self.cursor.execute("UPDATE inventory SET qty=qty-(?), amount=rate*(qty-(?)) WHERE i_code=?",
                            (sales_qty, sales_qty2, i_code))
        self.connect.commit()

    def sales_entry(self, i_code):
        self.cursor.execute("SELECT i_code, descp, rate FROM inventory WHERE i_code=?", (i_code,))
        row = self.cursor.fetchall()
        return row

    def check_low_inventory(self, i_code):
        self.cursor.execute("SELECT qty FROM inventory WHERE i_code=?", (i_code,))
        row = self.cursor.fetchall()
        return row

    def item_code_check(self):
        self.cursor.execute("SELECT i_code FROM inventory")
        row = self.cursor.fetchall()
        return row

    def reflection_from_update(self, i_code, qty, qty2):
        self.cursor.execute("UPDATE inventory SET qty=qty + (?), amount=(qty+?) * rate WHERE i_code=?",
                            (qty, qty2, i_code))
        self.connect.commit()

    def sales_deletion_reflection(self, i_code, qty, qty2):
        self.cursor.execute("UPDATE inventory SET qty=qty+(?), amount=(qty+?) * rate WHERE i_code=?",
                            (qty, qty2, i_code))
        self.connect.commit()

    # ======================= Purchases Data ===============================
    def update_inv_from_purchases(self, i_code, pur_qty, pur_qty2):
        self.cursor.execute("UPDATE inventory SET qty=qty + (?), amount=(qty+?) * rate WHERE i_code=?",
                            (pur_qty, pur_qty2, i_code))
        self.connect.commit()

    def purchase_deletion_reflection(self, i_code, qty, qty2):
        self.cursor.execute("UPDATE inventory SET qty=qty-?, amount=(qty-?) * rate WHERE i_code=?",
                            (qty, qty2, i_code))
        self.connect.commit()

    # ==================== Inventory Report =============================
    def report(self, s_date, e_date):
        self.cursor.execute("SELECT item_no, date, i_code, descp, amount FROM inventory WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def sum_amt(self, s_date, e_date):
        self.cursor.execute("SELECT SUM (amount) FROM inventory WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def close_database(self):
        self.connect.close()


class TrackInventoryData:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS t_inventory(id INTEGER PRIMARY KEY, item_no TEXT, date DATE,"
                            "i_code TEXT, description TEXT, unit TEXT, rate TEXT, qty REAL, amount TEXT, rmks TEXT,"
                            "user_action TEXT)")
        self.connect.commit()

    def insert(self, item_no, date, i_code, description, unit, rate, qty, amount, rmks, user_action):
        self.cursor.execute("INSERT INTO t_inventory VALUES(NULL, ?,?,?,?,?,?,?,?,?,?)",
                            (item_no, date, i_code, description, unit, rate, qty, amount, rmks, user_action))
        self.connect.commit()

    def display(self):
        self.cursor.execute("SELECT * FROM t_inventory")
        row = self.cursor.fetchall()
        return row

    def search_with_item_code(self, i_code):
        self.cursor.execute("SELECT * FROM t_inventory WHERE i_code=?", (i_code,))
        row = self.cursor.fetchall()
        return row

    def search_with_action(self, user_action):
        self.cursor.execute("SELECT * FROM t_inventory WHERE user_action=?", (user_action,))
        row = self.cursor.fetchall()
        return row

    def item_code_check(self):
        self.cursor.execute("SELECT i_code FROM t_inventory")
        row = self.cursor.fetchall()
        return row

    def action_check(self):
        self.cursor.execute("SELECT user_action FROM t_inventory")
        row = self.cursor.fetchall()
        return row

    def close_database(self):
        self.connect.close()
