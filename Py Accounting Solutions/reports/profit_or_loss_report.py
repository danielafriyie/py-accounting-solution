from tkinter import *
from tkinter import ttk
from sales import sales_data
from expenditure import expenditure_data

s_data = sales_data.SalesData(r"sales_database.db")
e_data = expenditure_data.ExpensesData(r"exp_data.db")


class ProfitOrLoss(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Profit or Loss")
        self.label = ttk.Label(self, text="PROFIT OR LOSS", font=("Times New Roman", 40, "bold"))
        self.label.pack()

        self.date_entry_frame = ttk.Frame(self)
        self.date_entry_frame.pack(anchor=W)

        self.start_date_label = ttk.Label(self.date_entry_frame, text="Start Date")
        self.start_date_label.grid(row=0, column=0, sticky=W)
        self.start_date_entry = ttk.Entry(self.date_entry_frame, )
        self.start_date_entry.grid(row=0, column=1, sticky=W, padx=5)

        self.end_date_label = ttk.Label(self.date_entry_frame, text="End Date")
        self.end_date_label.grid(row=1, column=0, sticky=W)
        self.end_date_entry = ttk.Entry(self.date_entry_frame, )
        self.end_date_entry.grid(row=1, column=1, sticky=W, padx=5)

        self.click_me = ttk.Label(self.date_entry_frame, text="Generate Report")
        self.click_me.grid(row=2, column=0, sticky=W)
        self.click_me_btn = ttk.Button(self.date_entry_frame, width=19, text="Click me!",
                                       command=self.click_me_btn_command)
        self.click_me_btn.grid(row=2, column=1, sticky=W, padx=5)

        self.frame = ttk.Frame(self)
        self.frame.pack(expand=True, fill=BOTH)

        self.display_tree = ttk.Treeview(self.frame)
        self.display_tree.pack(expand=True, fill=BOTH)

        self.display_tree.column("#0", anchor=CENTER)
        # self.display_tree.heading("#0", text="Profit or Loss")
        # self.display_tree.insert("", END, "revenue", text="Revenue")
        # self.display_tree.insert("", END, "expenditure", text="Expenditure")
        self.columns = ("des", "amt1", "amt2")
        self.headings = ("Description", "GH¢", "GH¢")
        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "des":
                col_width = 250
            elif col == "amt1":
                col_width = 100
            elif col == "amt2":
                col_width = 100
            self.display_tree.column(col, width=col_width, anchor=CENTER)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    def click_me_btn_command(self):
        try:
            for children in self.display_tree.get_children():
                self.display_tree.delete(children)
            self.display_tree.insert("", END, "revenue", text="Revenue")
            self.display_tree.insert("", END, "expenditure", text="Expenditure")
            self.display_tree.item("revenue", open=True)
            self.display_tree.item("expenditure", open=True)
            revenue_amt = s_data.sum_amt(self.start_date_entry.get(), self.end_date_entry.get())[0][0]
            exp_amt = e_data.sum_amt(self.start_date_entry.get(), self.end_date_entry.get())[0][0]
            p_or_l = revenue_amt - exp_amt
            print(p_or_l)
            for data in s_data.revenue(self.start_date_entry.get(), self.end_date_entry.get()):
                # print(data)
                self.display_tree.insert("revenue", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.insert("revenue", END, revenue_amt, text="Total")
            self.display_tree.set(revenue_amt, self.columns[2], revenue_amt)

            for data in e_data.expenses(self.start_date_entry.get(), self.end_date_entry.get()):
                # print(data)
                self.display_tree.insert("expenditure", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.insert("expenditure", END, exp_amt, text="Total")
            self.display_tree.set(exp_amt, self.columns[2], "(" + str(exp_amt) + ")")

            self.display_tree.insert("", END, p_or_l, text="Profit or Loss")
            self.display_tree.set(p_or_l, self.columns[2], p_or_l)
        except TypeError:
            print("TypeError: << check click_me_btn_command method >>")
