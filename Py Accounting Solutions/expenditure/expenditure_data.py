import sqlite3 as sq


class ExpensesData:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS exp_data(id INTEGER PRIMARY KEY, exp_id TEXT, date DATE, "
                            "des TEXT, amt REAL)")
        self.connect.commit()

    def add_new(self, exp_id, date, des, amt):
        self.cursor.execute("INSERT INTO exp_data VALUES(NULL, ?,?,?,?)", (exp_id, date, des, amt))
        self.connect.commit()

    def update(self, exp_id, date, des, amt):
        self.cursor.execute("UPDATE exp_data SET date=?, des=?, amt=? WHERE exp_id=?", (date, des, amt, exp_id))
        self.connect.commit()

    def delete(self, exp_id):
        self.cursor.execute("DELETE FROM exp_data WHERE exp_id=?", (exp_id,))
        self.connect.commit()

    def display_all(self):
        self.cursor.execute("SELECT * FROM exp_data")
        row = self.cursor.fetchall()
        return row

    def edit(self, exp_id):
        self.cursor.execute("SELECT * FROM exp_data WHERE exp_id=?", (exp_id,))
        row = self.cursor.fetchall()
        return row

    def exp_id_gen(self):
        self.cursor.execute("SELECT id FROM exp_data ORDER BY id DESC")
        row = self.cursor.fetchall()
        return row

    def exp_id_check(self):
        self.cursor.execute("SELECT exp_id FROM exp_data")
        row = self.cursor.fetchall()
        return row

    def display_exp_id(self):
        self.cursor.execute("SELECT exp_id FROM exp_data ORDER BY exp_id ASC")
        row = self.cursor.fetchall()
        return row

    def search_by_id(self, exp_id):
        self.cursor.execute("SELECT exp_id FROM exp_data WHERE exp_id=?", (exp_id,))
        row = self.cursor.fetchall()
        return row

    # ==================== Expense Report =============================
    def report(self, s_date, e_date):
        self.cursor.execute("SELECT exp_id, date, des, amt FROM exp_data WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def sum_amt(self, s_date, e_date):
        self.cursor.execute("SELECT SUM (amt) FROM exp_data WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def expenses(self, s_date, e_date):
        self.cursor.execute("SELECT exp_id, des, amt FROM exp_data WHERE date BETWEEN ? AND ?", (s_date, e_date))
        return self.cursor.fetchall()

    def close_database(self):
        self.connect.close()


class TrackExpenditure:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS track_exp(id INTEGER PRIMARY KEY, exp_id TEXT, date DATE, "
                            "des TEXT, amt REAL, user_action TEXT)")
        self.connect.commit()

    def insert(self, exp_id, date, des, amt, user_action):
        self.cursor.execute("INSERT INTO track_exp VALUES(NULL, ?,?,?,?,?)", (exp_id, date, des, amt, user_action))
        self.connect.commit()

    def display_all(self):
        self.cursor.execute("SELECT * FROM track_exp")
        row = self.cursor.fetchall()
        return row

    def search_by_id(self, exp_id):
        self.cursor.execute("SELECT * FROM track_exp WHERE exp_id=?", (exp_id,))
        row = self.cursor.fetchall()
        return row

    def search_by_user_action(self, user_action):
        self.cursor.execute("SELECT * FROM track_exp WHERE user_action=?", (user_action,))
        row = self.cursor.fetchall()
        return row

    def id_check(self):
        self.cursor.execute("SELECT exp_id FROM track_exp")
        row = self.cursor.fetchall()
        return row

    def user_action_check(self):
        self.cursor.execute("SELECT user_action FROM track_exp")
        row = self.cursor.fetchall()
        return row

    def close_database(self):
        self.connect.close()
