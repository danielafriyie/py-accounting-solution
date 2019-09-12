from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbx
from datetime import datetime as dt
from expenditure import expenditure_data

e_data = expenditure_data.ExpensesData(r"exp_data.db")
t_expenses = expenditure_data.TrackExpenditure(r"tack_exp_data.db")


class Expenses(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Expenditure Window")
        self.grab_set()

        self.select_exp_frame = LabelFrame(self, text="Select Expense")
        self.select_exp_frame.pack(fill=BOTH, side=LEFT, anchor=N)

        self.expense_entry_frame = LabelFrame(self, text="Expense Entry")
        self.expense_entry_frame.pack(fill=BOTH, anchor=N)

        self.expense_description_frame = LabelFrame(self, text="Description")
        self.expense_description_frame.pack(expand=True, fill=BOTH, side=BOTTOM)

        # ============ Expense Search and Listbox ===============================
        self.exp_search = ttk.Entry(self.select_exp_frame, width=23)
        self.exp_search.pack(anchor=N)
        self.exp_search.bind("<Return>", self.search_command)

        self.exp_box = Listbox(self.select_exp_frame)
        self.exp_box.pack(expand=True, fill=Y, side=LEFT)
        self.exp_box.bind('<<ListboxSelect>>', self.exp_box_select)

        # Inserts exp_id into exp_box in alph order
        for data in e_data.display_exp_id():
            for _id in data:
                self.exp_box.insert(END, _id)

        self.exp_box_scroll = ttk.Scrollbar(self.select_exp_frame)
        self.exp_box_scroll.pack(expand=True, fill=Y, side=LEFT)
        self.exp_box.config(yscrollcommand=self.exp_box_scroll.set)
        self.exp_box_scroll.config(command=self.exp_box.yview)

        # =============== Expense Entry ========================================
        self.date_label = ttk.Label(self.expense_entry_frame, text="Date")
        self.date_label.grid(row=0, column=0, sticky=W)
        self.date_entry = ttk.Entry(self.expense_entry_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, sticky=W)
        self.date_entry.insert(END, dt.today().date())

        self.des_label = ttk.Label(self.expense_entry_frame, text="Description", )
        self.des_label.grid(row=1, column=0, sticky=W)
        self.des_entry = ttk.Entry(self.expense_entry_frame, width=40)
        self.des_entry.grid(row=1, column=1, padx=5, sticky=W)

        self.amt_label = ttk.Label(self.expense_entry_frame, text="Amount", )
        self.amt_label.grid(row=2, column=0, sticky=W)
        self.amt_entry = ttk.Entry(self.expense_entry_frame, width=15)
        self.amt_entry.grid(row=2, column=1, padx=5, sticky=W)

        self.exp_id_btn = ttk.Button(self.expense_entry_frame, text="Expense ID", width=10,
                                     command=self.exp_id_btn_command)
        self.exp_id_btn.grid(row=3, column=0)
        self.exp_id_entry = ttk.Entry(self.expense_entry_frame)
        self.exp_id_entry.grid(row=3, column=1, sticky=W, padx=5)

        # =================== Expense Description =========================================
        self.display_tree = ttk.Treeview(self.expense_description_frame)
        self.display_tree.pack(side=LEFT, expand=True, fill=BOTH)

        self.display_tree_scroll = ttk.Scrollbar(self.expense_description_frame)
        self.display_tree_scroll.pack(side=LEFT, fill=Y)
        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)
        self.display_tree_scroll.config(command=self.display_tree.yview)

        self.add_new_btn = Button(self.expense_description_frame, width=10, text="Add New", relief=RIDGE,
                                  command=self.add_new_btn_command)
        self.add_new_btn.pack(anchor=N, padx=5, pady=5)

        self.update_btn = Button(self.expense_description_frame, width=10, text="Update", relief=RIDGE,
                                 command=self.update_btn_command)
        self.update_btn.pack(anchor=N, padx=5, pady=5)

        self.delete_btn = Button(self.expense_description_frame, width=10, text="Delete", relief=RIDGE,
                                 command=self.delete_btn_command)
        self.delete_btn.pack(anchor=N, padx=5, pady=5)

        self.edit_btn = Button(self.expense_description_frame, width=10, text="Edit", relief=RIDGE,
                               command=self.edit_btn_command)
        self.edit_btn.pack(anchor=N, padx=5, pady=5)

        self.cancel_btn = Button(self.expense_description_frame, width=10, text="Cancel", relief=RIDGE,
                                 command=self.cancel_btn_command)
        self.cancel_btn.pack(anchor=N, padx=5, pady=5)

        self.refresh_btn = Button(self.expense_description_frame, width=10, text="Refresh", relief=RIDGE,
                                  command=self.refresh_btn_command)
        self.refresh_btn.pack(anchor=N, padx=5, pady=5)

        self.close_btn = Button(self.expense_description_frame, width=10, text="Close", relief=RIDGE,
                                command=self.destroy)
        self.close_btn.pack(anchor=N, padx=5, pady=5)

        self.columns = ("date", "des", "amt")
        self.headings = ("Date", "Description", "Amount")

        self.display_tree.column("#0", anchor=CENTER, width=100)
        self.display_tree.heading("#0", text="Expense ID")
        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "date":
                col_width = 80
            elif col == "des":
                col_width = 350
            elif col == "amt":
                col_width = 100
            self.display_tree.column(col, width=col_width, anchor=CENTER)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    def add_new_btn_command(self):
        print(e_data.exp_id_check())
        if self.exp_id_entry.get() == "" or self.date_entry.get() == "" or self.des_entry.get() == "" or \
                self.amt_entry.get() == "":
            mbx.showinfo("", "Incomplete data\nPlease fill all the necessary entries")
        elif (self.exp_id_entry.get(),) in e_data.exp_id_check():
            mbx.showinfo("Duplicate Entry", "ID already exist")
        else:
            e_data.add_new(
                self.exp_id_entry.get(),
                self.date_entry.get(),
                self.des_entry.get(),
                self.amt_entry.get()
            )
            t_expenses.insert(
                self.exp_id_entry.get(),
                self.date_entry.get(),
                self.des_entry.get(),
                self.amt_entry.get(),
                user_action="New Data"
            )
            mbx.showinfo("Saved Alert", "Saved Successfully")

    def exp_id_btn_command(self):
        self.exp_id_entry.delete(0, END)
        try:
            __id = e_data.exp_id_gen()
            print(__id[0][0])
            if len(str(__id[0][0])) == 1:
                exp_id = "EXP000" + str(__id[0][0] + 1)
                self.exp_id_entry.insert(END, exp_id)
            elif len(str(__id[0][0])) == 2:
                exp_id = "EXP00" + str(__id[0][0] + 1)
                self.exp_id_entry.insert(END, exp_id)
            elif len(str(__id[0][0])) == 3:
                exp_id = "EXP0" + str(__id[0][0] + 1)
                self.exp_id_entry.insert(END, exp_id)
            elif len(str(__id[0][0])) == 4:
                exp_id = "EXP" + str(__id[0][0] + 1)
                self.exp_id_entry.insert(END, exp_id)
        except IndexError:
            self.exp_id_entry.insert(END, "EXP0001")

    def refresh_btn_command(self):
        print(e_data.display_all())
        self.exp_box.delete(0, END)
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        for data in e_data.display_all():
            self.display_tree.insert("", END, data[1], text=data[1])
            self.display_tree.set(data[1], self.columns[0], data[2])
            self.display_tree.set(data[1], self.columns[1], data[3])
            self.display_tree.set(data[1], self.columns[2], data[4])
            # Inserts exp_id into exp_box in alph order
        for data in e_data.display_exp_id():
            for _id in data:
                self.exp_box.insert(END, _id)

    def cancel_btn_command(self):
        # self.date_entry.delete(0, END)
        self.des_entry.delete(0, END)
        self.amt_entry.delete(0, END)
        self.exp_id_entry.delete(0, END)

    def update_btn_command(self):
        if self.exp_id_entry.get() == "" or self.date_entry.get() == "" or self.des_entry.get() == "" or \
                self.amt_entry.get() == "":
            mbx.showinfo("", "Incomplete data\nPlease fill all the necessary entries")
        else:
            e_data.update(
                self.exp_id_entry.get(),
                self.date_entry.get(),
                self.des_entry.get(),
                self.amt_entry.get()
            )
            t_expenses.insert(
                self.exp_id_entry.get(),
                self.date_entry.get(),
                self.des_entry.get(),
                self.amt_entry.get(),
                user_action="Updated Data"
            )
            mbx.showinfo("Updated Alert", "Updated Successfully")

    def delete_btn_command(self):
        try:
            index = self.display_tree.selection()
            print(index[0])
            for data in e_data.edit(index[0]):
                print(data)
                t_expenses.insert(
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    user_action="Deleted Data"
                )
            e_data.delete(index[0])
            mbx.showinfo("Deleted Alert", "Deleted Successfully")
        except IndexError:
            print("IndexError: 'index' variable is empty <<check delete button command>>")
            mbx.showinfo("Nothing Selected Alert", "You have not selected anything")

    def edit_btn_command(self):
        self.exp_id_entry.delete(0, END)
        self.des_entry.delete(0, END)
        self.amt_entry.delete(0, END)
        try:
            index = self.display_tree.selection()
            for data in e_data.edit(index[0]):
                print(data)
                self.des_entry.insert(END, data[3])
                self.amt_entry.insert(END, data[4])
                self.exp_id_entry.insert(END, data[1])
        except IndexError:
            print("IndexError: 'index' variable is empty <<check edit button command>>")
            mbx.showinfo("Nothing Selected Alert", "You have not selected anything")

    def exp_box_select(self, event):
        self.exp_id_entry.delete(0, END)
        self.des_entry.delete(0, END)
        self.amt_entry.delete(0, END)
        try:
            index = self.exp_box.curselection()[0]
            selected_row = self.exp_box.get(index)
            print(selected_row)
            for data in e_data.edit(selected_row):
                self.des_entry.insert(END, data[3])
                self.amt_entry.insert(END, data[4])
                self.exp_id_entry.insert(END, data[1])
        except IndexError:
            print("IndexError: 'index' variable is empty <<check exp_box_select method>>")

    def search_command(self, event):
        self.exp_box.delete(0, END)
        for data in e_data.search_by_id(self.exp_search.get()):
            self.exp_box.insert(END, data[0])


class TrackExpenditure(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Track Expenditure")
        self.grab_set()

        self.search = ttk.Label(self, text="Search", font=("Times New Roman", 13))
        self.search.pack()

        self.search_entry = ttk.Entry(self, width=40)
        self.search_entry.pack()
        self.search_entry.bind("<Return>", self.search_command)

        self.display_tree = ttk.Treeview(self)
        self.display_tree.pack(expand=True, fill=BOTH, side=LEFT)

        self.display_tree_scroll = ttk.Scrollbar(self, )
        self.display_tree_scroll.pack(side=LEFT, fill=Y)
        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)
        self.display_tree_scroll.config(command=self.display_tree.yview)

        self.refresh_btn = Button(self, text="Refresh", width=10, relief=RIDGE,
                                  command=self.refresh_btn_command)
        self.refresh_btn.pack(side=LEFT, anchor=N, padx=5)

        self.columns = ("e_id", "date", "des", "amt", "u_action")
        self.headings = ("Expense ID", "Date", "Description", "Amount", "Action")

        self.display_tree.column("#0", width=60, anchor=CENTER)
        self.display_tree.heading("#0", text="ID")

        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "e_id":
                col_width = 100
            elif col == "date":
                col_width = 100
            elif col == "des":
                col_width = 350
            elif col == "amt":
                col_width = 80
            elif col == "u_action":
                col_width = 100
            self.display_tree.column(col, anchor=CENTER, width=col_width)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    def refresh_btn_command(self):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        for data in t_expenses.display_all():
            print(data)
            self.display_tree.insert("", END, data[0], text=data[0])
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])

    def search_command(self, event):
        print(t_expenses.id_check())
        print(t_expenses.user_action_check())
        print(self.search_entry.get(),)
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        if (self.search_entry.get(),) in t_expenses.id_check():
            for data in t_expenses.search_by_id(self.search_entry.get()):
                print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
        elif (self.search_entry.get(),) in t_expenses.user_action_check():
            for data in t_expenses.search_by_user_action(self.search_entry.get()):
                print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
        else:
            mbx.showinfo("", "What you entered does not exist")
