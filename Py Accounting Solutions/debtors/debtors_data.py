import sqlite3 as sq


class AccountsReceivableData:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS accounts_data(id INTEGER PRIMARY KEY, date DATE, s_name TEXT, o_name TEXT, "
            "p_no TEXT, loc TEXT, res TEXT, a_no TEXT)")
        self.connect.commit()

    def save_btn(self, date, s_name, o_name, p_no, loc, res, a_no):
        self.cursor.execute("INSERT INTO accounts_data VALUES(NULL,?,?,?,?,?,?,?)",
                            (date, s_name, o_name, p_no, loc, res, a_no))
        self.connect.commit()

    def delete_btn(self, id):
        self.cursor.execute("DELETE FROM accounts_data WHERE id=?", (id,))
        self.connect.commit()

    def edit_btn(self, id):
        self.cursor.execute("SELECT * FROM accounts_data WHERE id=?", (id,))
        row = self.cursor.fetchall()
        return row

    def update_btn(self, id, date, s_name, o_name, p_no, loc, res, a_no):
        self.cursor.execute("UPDATE accounts_data SET date=?, s_name=?, o_name=?, p_no=?, loc=?, res=?, a_no=? "
                            "WHERE id=?", (date, s_name, o_name, p_no, loc, res, a_no, id))
        self.connect.commit()

    def search_with_code(self):
        self.cursor.execute("SELECT a_no FROM accounts_data")
        row = self.cursor.fetchall()
        return row

    def display_data(self):
        self.cursor.execute("SELECT * FROM accounts_data")
        row = self.cursor.fetchall()
        return row

    def get_selected_row(self, a_no):
        self.cursor.execute("SELECT * FROM accounts_data WHERE a_no=?", (a_no,))
        row = self.cursor.fetchall()
        return row

    def id_no_select(self):
        self.cursor.execute("SELECT id FROM accounts_data ORDER BY id DESC LIMIT 1")
        row = self.cursor.fetchall()
        return row

    def display_a_no(self):
        self.cursor.execute("SELECT a_no FROM accounts_data ORDER BY a_no ASC")
        row = self.cursor.fetchall()
        return row

    # ========================= Sales Window =======================
    def search_with_account_no(self, a_no):
        self.cursor.execute("SELECT s_name, o_name, res, loc FROM accounts_data WHERE a_no=?", (a_no,))
        row = self.cursor.fetchall()
        return row

    def customer_check(self, ):
        self.cursor.execute("SELECT a_no FROM accounts_data")
        row = self.cursor.fetchall()
        return row

    def close_database(self):
        self.connect.close()

    # ============================== View Account Window ==================================
    def account_data(self, a_no):
        self.cursor.execute("SELECT * FROM accounts_data WHERE a_no=?", (a_no,))
        row = self.cursor.fetchall()
        return row


class TrackDebtorsData:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS t_accounts_data(id INTEGER PRIMARY KEY, date DATE, s_name TEXT, "
            "o_name TEXT, p_no TEXT, loc TEXT, res TEXT, a_no TEXT, user_action TEXT)")
        self.connect.commit()

    def insert(self, date, s_name, o_name, p_no, loc, res, a_no, action):
        self.cursor.execute("INSERT INTO t_accounts_data VALUES(NULL, ?,?,?,?,?,?,?,?)",
                            (date, s_name, o_name, p_no, loc, res, a_no, action))
        self.connect.commit()

    def display(self):
        self.cursor.execute("SELECT * FROM t_accounts_data")
        row = self.cursor.fetchall()
        return row

    def a_no_search(self, a_no):
        self.cursor.execute("SELECT * FROM t_accounts_data WHERE a_no=?", (a_no,))
        row = self.cursor.fetchall()
        return row

    def close_database(self):
        self.connect.close()


class AccountData:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS account_data(id INTEGER PRIMARY KEY, account_no TEXT,"
                            "date DATE, i_code TEXT, inv_no, des TEXT, qty REAL , rte REAL, amt REAL)")
        self.connect.commit()

    def insert(self, account_no, date, i_code, inv_no, des, qty, rte, amt):
        self.cursor.execute("INSERT INTO account_data VALUES(NULL, ?,?,?,?,?,?,?,?)", (
            account_no, date, i_code, inv_no, des, qty, rte, amt)
                            )
        self.connect.commit()

    def update(self, i_code, des, qty, rte, amt, inv_no):
        self.cursor.execute(
            "UPDATE account_data SET i_code=?, des=?, qty=?, rte=?, amt=? WHERE inv_no=?",
            (
                i_code, des, qty, rte, amt, inv_no
            ))
        self.connect.commit()

    def delete(self, inv_no):
        self.cursor.execute("DELETE FROM account_data WHERE inv_no=?",
                            (inv_no,))
        self.connect.commit()

    def i_code_check(self):
        self.cursor.execute("SELECT i_code FROM account_data")
        row = self.cursor.fetchall()
        return row

    def display_all(self, account_no):
        self.cursor.execute("SELECT * FROM account_data WHERE account_no=?", (account_no,))
        row = self.cursor.fetchall()
        return row

    def invoice_amt_search(self, inv_no):
        self.cursor.execute("SELECT amt FROM account_data WHERE inv_no=?", (inv_no,))
        row = self.cursor.fetchall()
        return row

    def total_amt(self, account_no):
        self.cursor.execute("SELECT SUM(amt) FROM account_data WHERE account_no=?", (account_no,))
        row = self.cursor.fetchall()
        return row

    def select_i_code_with_inv_no(self, inv_no):
        self.cursor.execute("SELECT i_code FROM account_data WHERE inv_no=?", (inv_no,))
        row = self.cursor.fetchall()
        return row

    def full_payment(self, inv_no):
        self.cursor.execute("DELETE FROM account_data WHERE inv_no=?", (inv_no,))
        self.connect.commit()

    def half_payment(self, amt, inv_no):
        self.cursor.execute("UPDATE account_data SET amt=amt-? WHERE inv_no=?", (amt, inv_no))
        self.connect.commit()

    def part_payment_delete_reflection(self, amt, inv_no):
        self.cursor.execute("UPDATE account_data SET amt=amt+(?) WHERE inv_no=?", (amt, inv_no))
        self.connect.commit()

    def inv_no_check(self):
        self.cursor.execute("SELECT inv_no FROM account_data")
        return self.cursor.fetchall()

    def select_i_code(self, inv_no):
        self.cursor.execute("SELECT i_code FROM account_data WHERE inv_no=?", (inv_no,))
        row = self.cursor.fetchall()
        return row

    # ================= Accounts Receivable Report Window ========================================
    def report(self, s_date, e_date):
        self.cursor.execute(
            "SELECT id, date, inv_no, account_no, i_code, des, amt FROM account_data WHERE date BETWEEN ? AND ?",
            (s_date, e_date))
        return self.cursor.fetchall()

    def sum_amt(self, s_date, e_date):
        self.cursor.execute("SELECT SUM (amt) FROM account_data WHERE date BETWEEN ? AND ?",
                            (s_date, e_date))
        return self.cursor.fetchall()

    def close_database(self):
        self.connect.close()


class AccountHistory:

    def __init__(self, db):
        self.connect = sq.connect(db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS a_history(id INTEGER PRIMARY KEY, date DATE, i_code TEXT, "
                            "inv_no TEXT, a_no, payment_type TEXT, amt REAL, act TEXT)")
        self.connect.commit()

    def i_code_check(self):
        self.cursor.execute("SELECT i_code FROM a_history")
        return self.cursor.fetchall()

    def inv_no_check(self):
        self.cursor.execute("SELECT inv_no FROM a_history")
        return self.cursor.fetchall()

    def a_no_check(self):
        self.cursor.execute("SELECT a_no FROM a_history")
        return self.cursor.fetchall()

    def payment_type_check(self):
        self.cursor.execute("SELECT payment_type FROM a_history")
        return self.cursor.fetchall()

    def act_check(self):
        self.cursor.execute("SELECT act FROM a_history")
        return self.cursor.fetchall()

    def insert(self, date, i_code, inv_no, a_no, payment_type, amt, act):
        self.cursor.execute("INSERT INTO a_history VALUES (NULL, ?,?,?,?,?,?,?)", (
            date, i_code, inv_no, a_no, payment_type, amt, act
        ))
        self.connect.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM a_history WHERE id=?", (id,))
        self.connect.commit()

    def select_inv_and_amt(self, id):
        self.cursor.execute("SELECT inv_no, amt FROM a_history WHERE id=?", (id,))
        return self.cursor.fetchall()

    def display_all(self):
        self.cursor.execute("SELECT * FROM a_history")
        return self.cursor.fetchall()

    def search_with_i_code(self, i_code):
        self.cursor.execute("SELECT * FROM a_history WHERE i_code=?", (i_code,))
        row = self.cursor.fetchall()
        return row

    def search_with_inv_no(self, inv_no):
        self.cursor.execute("SELECT * FROM a_history WHERE inv_no=?", (inv_no,))
        row = self.cursor.fetchall()
        return row

    def search_with_acc_no(self, a_no):
        self.cursor.execute("SELECT * FROM a_history WHERE a_no=?", (a_no,))
        row = self.cursor.fetchall()
        return row

    def search_with_type(self, payment_type):
        self.cursor.execute("SELECT * FROM a_history WHERE payment_type=?", (payment_type,))
        row = self.cursor.fetchall()
        return row

    def search_with_action(self, act):
        self.cursor.execute("SELECT * FROM a_history WHERE act=?", (act,))
        return self.cursor.fetchall()

    def id_search(self, id):
        self.cursor.execute("SELECT * FROM a_history WHERE id=?", (id,))
        return self.cursor.fetchall()

    def close_database(self):
        self.connect.close()
