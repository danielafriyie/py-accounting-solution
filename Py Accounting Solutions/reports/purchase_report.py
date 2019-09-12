from tkinter import *
from tkinter import ttk
from purchases import purchase_data

p_data = purchase_data.PurchasesData(r"purchases_database.db")


class PurchaseReport(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Purchases Report")
        self.exp_acc_label = ttk.Label(self, text="PURCHASES", font=("Times New Roman", 35, "bold"))
        self.exp_acc_label.pack()

        self.search_frame = ttk.Frame(self, )
        self.search_frame.pack(anchor=W)

        self.start_date_label = ttk.Label(self.search_frame, text="Start Date")
        self.start_date_label.grid(row=0, column=0, sticky=W, padx=5)
        self.start_date_entry = ttk.Entry(self.search_frame)
        self.start_date_entry.grid(row=0, column=1, sticky=W)

        self.end_date_label = ttk.Label(self.search_frame, text="End Date")
        self.end_date_label.grid(row=1, column=0, sticky=W, padx=5)
        self.end_date_entry = ttk.Entry(self.search_frame)
        self.end_date_entry.grid(row=1, column=1, sticky=W)

        self.click_me = ttk.Label(self.search_frame, text="Generate Report")
        self.click_me.grid(row=2, column=0, sticky=W, padx=5)
        self.search_btn = ttk.Button(self.search_frame, text="Click me!", width=19,
                                     command=self.generate_report_btn_command)
        self.search_btn.grid(row=2, column=1, stick=W)

        self.frame = ttk.Frame(self, )
        self.frame.pack(expand=True, fill=BOTH)

        self.display_tree = ttk.Treeview(self.frame, )
        self.display_tree.pack(fill=BOTH, expand=True, side=LEFT)
        self.display_tree_scroll = ttk.Scrollbar(self.frame)
        self.display_tree_scroll.pack(side=LEFT, fill=Y)
        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)
        self.display_tree_scroll.config(command=self.display_tree.yview)

        self.display_tree.column("#0", width=25, anchor=CENTER)
        self.display_tree.heading("#0", text="ID")

        self.total_frame = ttk.Frame(self)
        self.total_frame.pack(anchor=E, padx=19)

        self.total_label = ttk.Label(self.total_frame, text="Total Amount GH¢", font=("Times New Roman", 16, "bold"))
        self.total_label.grid(row=0, column=0, padx=10)
        self.total_entry = ttk.Entry(self.total_frame, width=30, font=("Times New Roman", 16, "bold"), justify=CENTER)
        self.total_entry.grid(row=0, column=1)

        self.columns = ("date", "inv_no", "a_no", "i_no", "ced")
        self.headings = ("Date", "Invoice No", "Account No", "Item No", "Amount GH¢")

        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "date":
                col_width = 100
            elif col == "inv_no":
                col_width = 100
            elif col == "a_no":
                col_width = 100
            elif col == "i_no":
                col_width = 80
            elif col == "ced":
                col_width = 80
            self.display_tree.column(col, width=col_width, anchor=CENTER)

        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    def generate_report_btn_command(self):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        self.total_entry.delete(0, END)
        for data in p_data.report(self.start_date_entry.get(), self.end_date_entry.get()):
            print(data)
            self.display_tree.insert("", END, data[0], text=data[0])
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])
        total_amt = (p_data.sum_amt(self.start_date_entry.get(), self.end_date_entry.get()))
        self.total_entry.insert(END, total_amt[0][0])
