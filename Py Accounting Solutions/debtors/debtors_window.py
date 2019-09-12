from tkinter import *
from tkinter import ttk
from datetime import datetime as dt
from tkinter import messagebox as mbx
from debtors import debtors_data
from inventory import inventory_data
from sales import sales_data

d_data = debtors_data.AccountsReceivableData(r"debtors_data.db")
t_debtors = debtors_data.TrackDebtorsData(r"track_debtors.db")
debtor = debtors_data.AccountData(r"accounts.db")
debtor_history = debtors_data.AccountHistory(r"account_history.db")
i_data = inventory_data.InventoryDatabase(r"inventory_data.db")
s_data = sales_data.SalesData(r"sales_database.db")


class Accounts(Toplevel):
    """
        Debtors Accounts
            * Add new account
            * Delete account
            * Update account
    """

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Accounts Receivable")
        self.config(background="light blue")
        self.grab_set()

        # self.frame = Frame(self).pack()

        self.data_input_frame_box = LabelFrame(self, text="Select Account")
        self.data_input_frame_box.pack(side=LEFT, anchor=N, fill=BOTH)

        self.data_input_frame = LabelFrame(self, text="Account Entry")
        self.data_input_frame.pack(anchor=N, fill=BOTH)

        self.details_box_frame = LabelFrame(self, text="Account Description")
        self.details_box_frame.pack(side=BOTTOM, expand=True, fill=BOTH)

        self.details_btn_frame = Frame(self)
        self.details_btn_frame.pack()

        # ============= Account Code Box with Search Entry ===================
        self.search = Entry(self.data_input_frame_box, width=23)
        self.search.pack()
        self.search.bind("<Return>", self.search_command)

        self.account_code_box = Listbox(self.data_input_frame_box, )
        self.account_code_box.pack(side=LEFT, anchor=N, expand=True, fill=Y)
        self.account_code_box.bind('<<ListboxSelect>>', self.selected_data)

        ##################################################
        # INSERT ACCOUNT NUMBER INTO self.account_code_box
        #################################################
        for data in d_data.display_data():
            self.account_code_box.insert(END, data[7])

        self.account_code_box_scrollbar = ttk.Scrollbar(self.data_input_frame_box)
        self.account_code_box.configure(yscrollcommand=self.account_code_box_scrollbar.set)
        self.account_code_box_scrollbar.configure(command=self.account_code_box.yview)
        self.account_code_box_scrollbar.pack(fill=Y, side=RIGHT, anchor=N)

        # ==================== Account entry ========================
        self.date_label = Label(self.data_input_frame, text="Date")
        self.date_label.grid(row=0, column=0, sticky=W)
        self.date_entry = Entry(self.data_input_frame, )
        self.date_entry.grid(row=0, column=1, sticky=W)

        self.surname_label = Label(self.data_input_frame, text="Surname")
        self.surname_label.grid(row=1, column=0, sticky=W)
        self.surname_entry = Entry(self.data_input_frame)
        self.surname_entry.grid(row=1, column=1, sticky=W)

        self.other_name_label = Label(self.data_input_frame, text="Other Names")
        self.other_name_label.grid(row=2, column=0, sticky=W)
        self.other_name_entry = Entry(self.data_input_frame, width=50)
        self.other_name_entry.grid(row=2, column=1, sticky=W)

        self.phone_no_label = Label(self.data_input_frame, text="Phone No.")
        self.phone_no_label.grid(row=3, column=0, sticky=W)
        self.phone_no_entry = Entry(self.data_input_frame, )
        self.phone_no_entry.grid(row=3, column=1, sticky=W)

        self.location_label = Label(self.data_input_frame, text="Location")
        self.location_label.grid(row=4, column=0, sticky=W)
        self.location_entry = Entry(self.data_input_frame)
        self.location_entry.grid(row=4, column=1, sticky=W)

        self.residence_label = Label(self.data_input_frame, text="Address")
        self.residence_label.grid(row=5, column=0, sticky=W)
        self.residence_entry = Entry(self.data_input_frame, )
        self.residence_entry.grid(row=5, column=1, sticky=W)

        self.account_no_label = ttk.Button(self.data_input_frame, text="Account No.",
                                           command=self.account_no_generation)
        self.account_no_label.grid(row=7, column=0, sticky=W, )
        self.account_no_entry = Entry(self.data_input_frame, )
        self.account_no_entry.grid(row=7, column=1, sticky=W)

        # ================= Account Description ==========================
        # Add ttk Tree view for the display of transactions
        self.display_tree = ttk.Treeview(self.details_box_frame, )
        self.display_tree.pack(side=LEFT, expand=True, fill=BOTH)
        self.display_tree_scroll = ttk.Scrollbar(self.details_box_frame, command=self.display_tree.yview)
        self.display_tree_scroll.pack(side=LEFT, fill=Y)
        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)

        self.save_btn = Button(self.details_box_frame, text="Save", width=10, relief=RIDGE,
                               command=self.save_btn_command)
        self.save_btn.pack(anchor=N, padx=5, pady=5)

        self.cancel_btn = Button(self.details_box_frame, text="Cancel", width=10, relief=RIDGE,
                                 command=self.cancel_btn_command)
        self.cancel_btn.pack(anchor=N, padx=5, pady=5)

        self.delete_btn = Button(self.details_box_frame, text="Delete", relief=RIDGE, width=10,
                                 command=self.delete_btn_command)
        self.delete_btn.pack(anchor=N, padx=5, pady=5)

        self.refresh_btn = Button(self.details_box_frame, text="Refresh", relief=RIDGE, width=10,
                                  command=self.refresh_btn_command)
        self.refresh_btn.pack(anchor=N, padx=5, pady=5)

        self.edit_btn = Button(self.details_box_frame, text="Edit", relief=RIDGE, width=10,
                               command=self.edit_btn_command)
        self.edit_btn.pack(anchor=N, padx=5, pady=5)

        self.update_btn = Button(self.details_box_frame, text="Update", relief=RIDGE, width=10,
                                 command=self.update_btn_command)
        self.update_btn.pack(anchor=N, padx=5, pady=5)

        # ================= Treeview Column names and headings ===============
        self.columns = ('date', 's_name', 'o_name', 'p_no', 'loc', 'rec', 'a_no')
        self.headings = ('Date', 'Surname', 'Other Names', 'Phone No.', 'Location', 'Address', 'Account No')
        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == 'date':
                col_width = 75
            elif col == "s_name":
                col_width = 180
            elif col == "o_name":
                col_width = 350
            elif col == "p_no":
                col_width = 80
            elif col == "loc":
                col_width = 100
            elif col == 'rec':
                col_width = 100
            elif col == "a_no":
                col_width = 80

            self.display_tree.column(col, width=col_width, anchor=CENTER)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1
        self.display_tree.column('#0', width=100, anchor=CENTER)
        self.display_tree.heading("#0", text="Account ID")

        ######################################################
        # BUTTON COMMANDS AND INTERACTIONS TO THE DATABASE
        ######################################################
        """ Inserts the current date to the date entry column """
        self.current_date = dt.today()
        self.date_entry.delete(0, END)
        self.date_entry.insert(END, self.current_date.date())

    def account_no_generation(self):
        self.account_no_entry.delete(0, END)
        try:
            num = d_data.id_no_select()
            print(num[0][0])
            if len(str(num[0][0])) == 1:
                a_n = "DEB000" + str(num[0][0] + 1)
                self.account_no_entry.insert(END, a_n)
            elif len(str(num[0][0])) == 2:
                a_n = "DEB00" + str(num[0][0] + 1)
                self.account_no_entry.insert(END, a_n)
            elif len(str(num[0][0])) == 3:
                a_n = "DEB0" + str(num[0][0] + 1)
                self.account_no_entry.insert(END, a_n)
            elif len(str(num[0][0])) >= 4:
                a_n = "DEB" + str(num[0][0] + 1)
                self.account_no_entry.insert(END, a_n)
        except IndexError:
            a_n = "DEB0001"
            self.account_no_entry.insert(END, a_n)

    def save_btn_command(self):
        if self.surname_entry.get() == '' or self.other_name_entry.get() == '' or \
                self.phone_no_entry.get() == '' or self.location_entry.get() == '' or \
                self.residence_entry.get() == '' or self.account_no_entry.get() == '':
            mbx.showinfo("Incomplete Input", "Incomplete input\nPlease fill all the necessary entries")
        elif (self.account_no_entry.get(),) in d_data.search_with_code():
            mbx.showinfo("Duplicate Entry Alert", "Account Code already exist")
        else:
            d_data.save_btn(
                self.date_entry.get(),
                self.surname_entry.get(),
                self.other_name_entry.get(),
                self.phone_no_entry.get(),
                self.location_entry.get(),
                self.residence_entry.get(),
                self.account_no_entry.get()
            )

            # INSERTS SAVED DATA INTO TRACKING DATABASE
            t_debtors.insert(
                self.date_entry.get(),
                self.surname_entry.get(),
                self.other_name_entry.get(),
                self.phone_no_entry.get(),
                self.location_entry.get(),
                self.residence_entry.get(),
                self.account_no_entry.get(),
                action="New Data"
            )
            mbx.showinfo("Saved Alert", "Saved Successfully")

    def cancel_btn_command(self):
        self.surname_entry.delete(0, END)
        self.other_name_entry.delete(0, END)
        self.phone_no_entry.delete(0, END)
        self.location_entry.delete(0, END)
        self.residence_entry.delete(0, END)
        self.account_no_entry.delete(0, END)

    def refresh_btn_command(self):
        self.account_code_box.delete(0, END)
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        for data in d_data.display_data():
            self.display_tree.insert('', END, data[0], text=data[0])
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])
            self.display_tree.set(data[0], self.columns[5], data[6])
            self.display_tree.set(data[0], self.columns[6], data[7])

        for a_no in d_data.display_data():
            self.account_code_box.insert(END, a_no[7])

    def delete_btn_command(self):
        try:
            index = self.display_tree.selection()
            query = mbx.askyesno("Confirm Delete", "Do you want to delete the selected data?")
            if query is True:

                # INSERTS DELETED DATA INTO TRACKING DATABASE
                for data in d_data.edit_btn(index[0]):
                    t_debtors.insert(
                        self.date_entry.get(),
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        data[7],
                        action="Deleted Data"
                    )

                d_data.delete_btn(index[0])
                mbx.showinfo("Deleted Alert", "Deleted Successfully")
        except IndexError:
            mbx.showinfo("Nothing Selected Alert", "You have not selected anything")
            print("There is an IndexError: 'index' variable is null")

    def edit_btn_command(self):
        self.surname_entry.delete(0, END)
        self.other_name_entry.delete(0, END)
        self.phone_no_entry.delete(0, END)
        self.location_entry.delete(0, END)
        self.residence_entry.delete(0, END)
        self.account_no_entry.delete(0, END)
        try:
            index = self.display_tree.selection()
            for data in d_data.edit_btn(index[0]):
                self.surname_entry.insert(END, data[2])
                self.other_name_entry.insert(END, data[3])
                self.phone_no_entry.insert(END, data[4])
                self.location_entry.insert(END, data[5])
                self.residence_entry.insert(END, data[6])
                self.account_no_entry.insert(END, data[7])
        except IndexError:
            mbx.showinfo("Nothing Selected Alert", "You have not selected anything")
            print("IndexError: 'index' variable is null")

    def update_btn_command(self):
        try:
            index = self.display_tree.selection()
            if self.surname_entry.get() == '' or self.other_name_entry.get() == '' or \
                    self.phone_no_entry.get() == '' or self.location_entry.get() == '' or \
                    self.residence_entry.get() == '' or self.account_no_entry.get() == '':
                mbx.showinfo("Incomplete Data Alert", "Incomplete Input, please fill the necessary entries")
            else:
                d_data.update_btn(
                    index[0],
                    self.date_entry.get(),
                    self.surname_entry.get(),
                    self.other_name_entry.get(),
                    self.phone_no_entry.get(),
                    self.location_entry.get(),
                    self.residence_entry.get(),
                    self.account_no_entry.get()
                )
                # INSERTS UPDATED DATA INTO TRACKING DATABASE
                t_debtors.insert(
                    self.date_entry.get(),
                    self.surname_entry.get(),
                    self.other_name_entry.get(),
                    self.phone_no_entry.get(),
                    self.location_entry.get(),
                    self.residence_entry.get(),
                    self.account_no_entry.get(),
                    action="Updated Data"
                )
                mbx.showinfo("Update Alert", "Updated Successfully")
        except IndexError:
            mbx.showinfo("Update Error Alert", "Use edit to select data before updating it")
            print("IndexError")

    def selected_data(self, event):
        try:
            index = self.account_code_box.curselection()[0]
            selected_row = self.account_code_box.get(index)
            print(selected_row)
            data = d_data.get_selected_row(selected_row)
            self.surname_entry.delete(0, END)
            self.other_name_entry.delete(0, END)
            self.phone_no_entry.delete(0, END)
            self.location_entry.delete(0, END)
            self.residence_entry.delete(0, END)
            self.account_no_entry.delete(0, END)
            self.surname_entry.insert(END, data[0][2])
            self.other_name_entry.insert(END, data[0][3])
            self.phone_no_entry.insert(END, data[0][4])
            self.location_entry.insert(END, data[0][5])
            self.residence_entry.insert(END, data[0][6])
            self.account_no_entry.insert(END, data[0][7])
        except IndexError:
            print("IndexError: 'index' variable is null <<check selected_data method>>")
            pass

    def search_command(self, event):
        for code in d_data.search_with_code():
            if self.search.get() in code:
                self.account_code_box.delete(0, END)
                self.account_code_box.insert(END, self.search.get())


class TrackAccountsReceivable(Toplevel):
    """
        Accounts Receivable Tracking
            * Track new entries
            * Track deleted entries
            * Track updated entries
    """

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Accounts Receivable Tracking")
        self.grab_set()
        self.search = Label(self, text="Search", font=("Times New Roman", 13))
        self.search.pack()
        self.search_entry = Entry(self, width=40)
        self.search_entry.pack()
        self.search_entry.bind("<Return>", self.search_command)

        self.display_tree = ttk.Treeview(self, )
        self.display_tree.pack(expand=True, fill=BOTH, side=LEFT)

        self.display_tree_scroll = ttk.Scrollbar(self)
        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)
        self.display_tree_scroll.config(command=self.display_tree.yview)
        self.display_tree_scroll.pack(side=LEFT, anchor=N, fill=Y)

        self.refresh_btn = Button(self, text="Refresh", width=15, command=self.refresh_btn_command, relief=RIDGE)
        self.refresh_btn.pack(side=LEFT, anchor=N)

        # COLUMN AND HEADING NAMES FOR THE TREEVIEW
        self.columns = ("date", "s_name", "o_name", "p_no", "loc", "res", "a_no", "action")
        self.headings = (
            "Date", "Surname", "Other Name", "Phone No.", "Location", "Residence", "Account No.", "Action")

        self.display_tree.heading("#0", text="ID")
        self.display_tree.column("#0", width=55)

        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "date":
                col_width = 80
            elif col == "s_name":
                col_width = 150
            elif col == "o_name":
                col_width = 300
            elif col == "p_no":
                col_width = 100
            elif col == "loc":
                col_width = 150
            elif col == "res":
                col_width = 120
            elif col == "a_no":
                col_width = 150
            elif col == "action":
                col_width = 180
            self.display_tree.column(col, width=col_width, anchor=CENTER)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

        for elements in self.display_tree.get_children():
            self.display_tree.delete(elements)

    def refresh_btn_command(self):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        for data in t_debtors.display():
            self.display_tree.insert('', END, data[0], text=data[0])
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])
            self.display_tree.set(data[0], self.columns[5], data[6])
            self.display_tree.set(data[0], self.columns[6], data[7])
            self.display_tree.set(data[0], self.columns[7], data[8])

    def search_command(self, event):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        if (self.search_entry.get(),) in d_data.customer_check():
            for data in t_debtors.a_no_search(self.search_entry.get()):
                print(data)
                self.display_tree.insert('', END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])
                self.display_tree.set(data[0], self.columns[7], data[8])
        else:
            mbx.showinfo("", "Account No. does not exist")


class ViewAccount(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Debtor's Account")
        self.grab_set()

        self.account_details_frame = LabelFrame(self, text="Accounts Details")
        self.account_details_frame.pack(fill=BOTH)

        self.sales_details_frame = LabelFrame(self, text="Sales Details")
        self.sales_details_frame.pack(fill=BOTH, expand=True)

        self.payment_details = LabelFrame(self, text="Payment Details")
        self.payment_details.pack(anchor=CENTER, fill=X)

        # =============== Account Details ======================================
        self.acc_no_label = ttk.Label(self.account_details_frame, text="Account No.")
        self.acc_no_label.grid(row=0, column=0, sticky=W)
        self.acc_no_entry = ttk.Entry(self.account_details_frame, )
        self.acc_no_entry.grid(row=0, column=1, sticky=W)
        self.acc_no_entry.bind("<Return>", self.account_no_search)

        self.type_label = ttk.Label(self.account_details_frame, text="Type")
        self.type_label.grid(row=0, column=2, sticky=W)
        self.type_entry = ttk.Combobox(self.account_details_frame, state="readonly", width=17)
        self.type_entry.grid(row=0, column=3, sticky=W)
        self.type_entry["value"] = ["", "Cash", "Cheque"]
        self.type_entry.bind("<<ComboboxSelected>>", self.cheque_no_entry_check)

        self.cheque_no_label = ttk.Label(self.account_details_frame, text="Cheque No.")
        self.cheque_no_label.grid(row=0, column=4)
        self.cheque_no_entry = ttk.Entry(self.account_details_frame, width=35, state=DISABLED)
        self.cheque_no_entry.grid(row=0, column=5)

        self.date_label = ttk.Label(self.account_details_frame, text="Date")
        self.date_label.grid(row=1, column=0, sticky=W)
        self.date_entry = ttk.Entry(self.account_details_frame)
        self.date_entry.grid(row=1, column=1, sticky=W)
        self.date_entry.insert(END, dt.today().date())

        self.address_label = ttk.Label(self.account_details_frame, text="Address")
        self.address_label.grid(row=1, column=2, sticky=W)
        self.address_entry = ttk.Entry(self.account_details_frame)
        self.address_entry.grid(row=1, column=3, sticky=W)

        self.surname_label = ttk.Label(self.account_details_frame, text="Surname")
        self.surname_label.grid(row=2, column=0, sticky=W)
        self.surname_entry = ttk.Entry(self.account_details_frame, width=25)
        self.surname_entry.grid(row=2, column=1, sticky=W)

        self.phone_no_label = ttk.Label(self.account_details_frame, text="Phone No.")
        self.phone_no_label.grid(row=2, column=2, sticky=W)
        self.phone_no_entry = ttk.Entry(self.account_details_frame)
        self.phone_no_entry.grid(row=2, column=3, sticky=W)

        self.other_name_label = ttk.Label(self.account_details_frame, text="Other Names")
        self.other_name_label.grid(row=3, column=0, sticky=W)
        self.other_name_entry = ttk.Entry(self.account_details_frame, width=40)
        self.other_name_entry.grid(row=3, column=1, sticky=W)

        self.location_label = ttk.Label(self.account_details_frame, text="Location")
        self.location_label.grid(row=3, column=2, sticky=W)
        self.location_entry = ttk.Entry(self.account_details_frame)
        self.location_entry.grid(row=3, column=3, sticky=W)

        # ========================= Display Tree_View ==========================
        self.display_tree = ttk.Treeview(self.sales_details_frame)
        self.display_tree.pack(expand=True, fill=BOTH, side=LEFT)
        self.display_tree_scroll = ttk.Scrollbar(self.sales_details_frame)
        self.display_tree_scroll.pack(side=LEFT, fill=Y)
        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)
        self.display_tree_scroll.config(command=self.display_tree.yview)

        # self.save_btn = Button(self.sales_details_frame, text="Save", relief=RIDGE, width=10)
        # self.save_btn.pack(anchor=N, padx=5, pady=5)

        self.refresh_btn = Button(self.sales_details_frame, text="Refresh", relief=RIDGE, width=10,
                                  command=self.refresh_btn_command)
        self.refresh_btn.pack(padx=5, anchor=N, pady=5)

        # self.update_btn = Button(self.sales_details_frame, text="Update", relief=RIDGE, width=10)
        # self.update_btn.pack(side=LEFT, anchor=N)
        #
        # self.delete_btn = Button(self.sales_details_frame, text="Delete", relief=RIDGE, width=10)
        # self.delete_btn.pack(side=LEFT, anchor=N)
        #
        # self.edit_btn = Button(self.sales_details_frame, text="Edit", relief=RIDGE, width=10)
        # self.edit_btn.pack(side=LEFT, anchor=N)

        self.cancel_btn = Button(self.sales_details_frame, text="Cancel", relief=RIDGE, width=10,
                                 command=self.cancel_btn_command)
        self.cancel_btn.pack(padx=5, anchor=N, pady=5)

        self.close_btn = Button(self.sales_details_frame, text="Close", relief=RIDGE, width=10, command=self.destroy)
        self.close_btn.pack(padx=5, anchor=N, pady=5)

        # ======================= Payment Details ======================
        self.total_label = ttk.Label(self.payment_details, text="Total")
        self.total_label.grid(row=0, column=0, sticky=W, padx=5, )
        self.total_entry = ttk.Entry(self.payment_details)
        self.total_entry.grid(row=0, column=1, sticky=W, padx=5)

        self.inv_label = ttk.Label(self.payment_details, text="Invoice No.")
        self.inv_label.grid(row=1, column=0, sticky=W, padx=5)
        self.inv_entry = ttk.Entry(self.payment_details, state=DISABLED)
        self.inv_entry.grid(row=1, column=1, sticky=W, padx=5)
        self.inv_entry.bind("<Return>", self.inv_no_search)

        self.payment_label = ttk.Label(self.payment_details, text="Payment Amount")
        self.payment_label.grid(row=2, column=0, sticky=W, padx=5)
        self.payment_entry = ttk.Entry(self.payment_details, state=DISABLED)
        self.payment_entry.grid(row=2, column=1, sticky=W, padx=5)

        self.balance_label = ttk.Label(self.payment_details, text="Balance")
        self.balance_label.grid(row=3, column=0, sticky=W, padx=5)
        self.balance_entry = ttk.Entry(self.payment_details, width=20, state=DISABLED)
        self.balance_entry.grid(row=3, column=1, sticky=W, padx=5)

        self.click_to_pay = ttk.Label(self.payment_details, text="Click to Pay")
        self.click_to_pay.grid(row=4, column=0, sticky=W, padx=5)
        self.click_to_pay_btn = ttk.Button(self.payment_details, text="Click me!", width=19,
                                           command=self.click_me_btn_command, state=DISABLED)
        self.click_to_pay_btn.grid(row=4, column=1, padx=5, sticky=W)

        self.columns = ("date", "i_code", "inv_no", "des", "qty", "rte", "amt", "dur")
        self.headings = ("Date", "Item Code", "Invoice No.", "Description", "Quantity", "Rate", "Amount", "Duration")

        self.display_tree.column("#0", width=60, anchor=CENTER)
        self.display_tree.heading("#0", text="ID")

        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "date":
                col_width = 80
            elif col == "i_code":
                col_width = 100
            elif col == "inv_no":
                col_width = 100
            elif col == "des":
                col_width = 350
            elif col == "qty":
                col_width = 80
            elif col == "rte":
                col_width = 80
            elif col == "amt":
                col_width = 100
            elif col == "dur":
                col_width = 100
            self.display_tree.column(col, width=col_width, anchor=CENTER)

        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    #######################################################################
    #               BUTTON COMMANDS
    #######################################################################
    def cancel_btn_command(self):
        self.type_entry.set("")
        self.payment_entry.delete(0, END)
        self.balance_entry.delete(0, END)
        self.inv_entry.delete(0, END)
        self.cheque_no_entry.delete(0, END)
        self.cheque_no_entry.config(state=DISABLED)
        self.inv_entry.config(state=DISABLED)
        self.payment_entry.config(state=DISABLED)
        self.balance_entry.config(state=DISABLED)
        self.click_to_pay_btn.config(state=DISABLED)

    def cheque_no_entry_check(self, event):
        if self.type_entry.get() == "Cheque":
            self.cheque_no_entry.config(state=NORMAL)
            self.inv_entry.config(state=NORMAL)
            self.payment_entry.config(state=NORMAL)
            self.balance_entry.config(state=NORMAL)
            self.click_to_pay_btn.config(state=NORMAL)
        elif self.type_entry.get() == "Cash":
            self.inv_entry.config(state=NORMAL)
            self.payment_entry.config(state=NORMAL)
            self.balance_entry.config(state=NORMAL)
            self.click_to_pay_btn.config(state=NORMAL)
        else:
            self.cheque_no_entry.config(state=DISABLED)
            self.inv_entry.config(state=DISABLED)
            self.payment_entry.config(state=DISABLED)
            self.balance_entry.config(state=DISABLED)
            self.click_to_pay_btn.config(state=DISABLED)

    def refresh_btn_command(self):
        try:
            for children in self.display_tree.get_children():
                self.display_tree.delete(children)
            self.surname_entry.delete(0, END)
            self.other_name_entry.delete(0, END)
            self.address_entry.delete(0, END)
            self.phone_no_entry.delete(0, END)
            self.location_entry.delete(0, END)
            for data in d_data.account_data(self.acc_no_entry.get()):
                # print(data)
                self.surname_entry.insert(END, data[2])
                self.other_name_entry.insert(END, data[3])
                self.phone_no_entry.insert(END, data[4])
                self.location_entry.insert(END, data[5])
                self.address_entry.insert(END, data[6])
            for data in debtor.display_all(self.acc_no_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[2])
                self.display_tree.set(data[0], self.columns[1], data[3])
                self.display_tree.set(data[0], self.columns[2], data[4])
                self.display_tree.set(data[0], self.columns[3], data[5])
                self.display_tree.set(data[0], self.columns[4], data[6])
                self.display_tree.set(data[0], self.columns[5], data[7])
                self.display_tree.set(data[0], self.columns[6], data[8])
                actual_date = dt.strptime(data[2], "%Y-%m-%d")
                self.display_tree.set(data[0], self.columns[7], (str((dt.today() - actual_date).days)) + " days")
            self.total_entry.delete(0, END)
            for data in debtor.total_amt(self.acc_no_entry.get()):
                # print(data[0])
                self.total_entry.insert(END, data[0])
        except Exception:
            # mbx.showinfo("", "Account number is empty")
            print("Exception: <<check refresh_btn_command method>>")
            pass

    def click_me_btn_command(self):
        try:
            item_code = debtor.select_i_code(self.inv_entry.get())[0][0]
            payment = "Cash"
            bal = debtor.invoice_amt_search(self.inv_entry.get())[0][0]
            payment_amt = float(self.payment_entry.get())
            print(bal)
            if self.type_entry.get() == "Cash":
                if self.payment_entry.get() != "":
                    if payment_amt == bal:
                        debtor.full_payment(self.inv_entry.get())
                        debtor_history.insert(
                            self.date_entry.get(),
                            item_code,
                            self.inv_entry.get(),
                            self.acc_no_entry.get(),
                            payment,
                            self.payment_entry.get(),
                            act="Full Payment"
                        )
                        mbx.showinfo("", "Successfully paid")
                        self.total_entry.delete(0, END)
                        self.inv_entry.delete(0, END)
                        self.payment_entry.delete(0, END)
                        self.balance_entry.delete(0, END)
                        for data in debtor.total_amt(self.acc_no_entry.get()):
                            # print(data[0])
                            self.total_entry.insert(END, data[0])
                    elif payment_amt < bal:
                        debtor.half_payment(payment_amt, self.inv_entry.get())
                        debtor_history.insert(
                            self.date_entry.get(),
                            item_code,
                            self.inv_entry.get(),
                            self.acc_no_entry.get(),
                            payment,
                            self.payment_entry.get(),
                            act="Part Payment"
                        )
                        mbx.showinfo("", "Successfully paid")
                        self.total_entry.delete(0, END)
                        self.inv_entry.delete(0, END)
                        self.payment_entry.delete(0, END)
                        self.balance_entry.delete(0, END)
                        for data in debtor.total_amt(self.acc_no_entry.get()):
                            # print(data[0])
                            self.total_entry.insert(END, data[0])
                    elif payment_amt > bal:
                        mbx.showinfo("Overpayment Alert", "Payment amount is greater than actual amount")
            elif self.type_entry.get() == "Cheque":
                if self.cheque_no_entry.get() != "":
                    if self.payment_entry.get() != "":
                        if payment_amt == bal:
                            debtor.full_payment(self.inv_entry.get())
                            debtor_history.insert(
                                self.date_entry.get(),
                                item_code,
                                self.inv_entry.get(),
                                self.acc_no_entry.get(),
                                self.cheque_no_entry.get(),
                                self.payment_entry.get(),
                                act="Full Payment"
                            )
                            mbx.showinfo("", "Successfully paid")
                            self.cheque_no_entry.delete(0, END)
                            self.total_entry.delete(0, END)
                            self.inv_entry.delete(0, END)
                            self.payment_entry.delete(0, END)
                            self.balance_entry.delete(0, END)
                            for data in debtor.total_amt(self.acc_no_entry.get()):
                                # print(data[0])
                                self.total_entry.insert(END, data[0])
                        elif payment_amt < bal:
                            debtor.half_payment(payment_amt, self.inv_entry.get())
                            debtor_history.insert(
                                self.date_entry.get(),
                                item_code,
                                self.inv_entry.get(),
                                self.acc_no_entry.get(),
                                self.cheque_no_entry.get(),
                                self.payment_entry.get(),
                                act="Part Payment"
                            )
                            mbx.showinfo("", "Successfully paid")
                            self.cheque_no_entry.delete(0, END)
                            self.total_entry.delete(0, END)
                            self.inv_entry.delete(0, END)
                            self.payment_entry.delete(0, END)
                            self.balance_entry.delete(0, END)
                            for data in debtor.total_amt(self.acc_no_entry.get()):
                                # print(data[0])
                                self.total_entry.insert(END, data[0])
                        elif payment_amt > bal:
                            mbx.showinfo("Overpayment Alert", "Payment amount is greater than actual amount")
                else:
                    mbx.showinfo("", "Enter cheque number")
        except IndexError:
            print("IndexError: <<check click_me_btn_command method>>")
            pass
        except ValueError:
            print("ValueError: <<check click_me_btn_command method>>")
            pass

    def account_no_search(self, event):
        try:
            if (self.acc_no_entry.get(),) in d_data.customer_check():
                for children in self.display_tree.get_children():
                    self.display_tree.delete(children)
                self.surname_entry.delete(0, END)
                self.other_name_entry.delete(0, END)
                self.address_entry.delete(0, END)
                self.phone_no_entry.delete(0, END)
                self.location_entry.delete(0, END)
                for data in d_data.account_data(self.acc_no_entry.get()):
                    # print(data)
                    self.surname_entry.insert(END, data[2])
                    self.other_name_entry.insert(END, data[3])
                    self.phone_no_entry.insert(END, data[4])
                    self.location_entry.insert(END, data[5])
                    self.address_entry.insert(END, data[6])
                for data in debtor.display_all(self.acc_no_entry.get()):
                    # print(data)
                    self.display_tree.insert("", END, data[0], text=data[0])
                    self.display_tree.set(data[0], self.columns[0], data[2])
                    self.display_tree.set(data[0], self.columns[1], data[3])
                    self.display_tree.set(data[0], self.columns[2], data[4])
                    self.display_tree.set(data[0], self.columns[3], data[5])
                    self.display_tree.set(data[0], self.columns[4], data[6])
                    self.display_tree.set(data[0], self.columns[5], data[7])
                    self.display_tree.set(data[0], self.columns[6], data[8])
                    actual_date = dt.strptime(data[2], "%Y-%m-%d")
                    self.display_tree.set(data[0], self.columns[7], (str((dt.today() - actual_date).days)) + " days")
                self.total_entry.delete(0, END)
                for data in debtor.total_amt(self.acc_no_entry.get()):
                    print(data[0])
                    self.total_entry.insert(END, data[0])
            else:
                mbx.showinfo("", "Account number does not exist!")
        except Exception:
            print("Exception: <<check account_no_search method>>")

    def inv_no_search(self, event):
        self.balance_entry.delete(0, END)
        for data in debtor.invoice_amt_search(self.inv_entry.get()):
            # print(data)
            self.balance_entry.insert(END, data[0])


class AccountHistory(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Account History")
        self.grab_set()

        self.search = ttk.Label(self, text="Search", font=("Times New Roman", 13))
        self.search.pack()
        self.search_entry = ttk.Entry(self, width=40)
        self.search_entry.pack()
        self.search_entry.bind("<Return>", self.search_command)

        self.details_frame = ttk.LabelFrame(self, text="Payment Details")
        self.details_frame.pack(expand=True, fill=BOTH)

        self.display_tree = ttk.Treeview(self.details_frame)
        self.display_tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.display_tree_scroll = ttk.Scrollbar(self.details_frame, command=self.display_tree.yview)
        self.display_tree_scroll.pack(side=LEFT, fill=Y)
        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)

        self.refresh_btn = ttk.Button(self.details_frame, text="Refresh", width=10, command=self.refresh_btn_command)
        self.refresh_btn.pack(anchor=N, padx=5, pady=5)

        self.delete_btn = ttk.Button(self.details_frame, text="Delete", width=10, command=self.delete_btn_command)
        self.delete_btn.pack(anchor=N, padx=5, pady=5)

        self.close_btn = ttk.Button(self.details_frame, text="Close", width=10, command=self.destroy)
        self.close_btn.pack(anchor=N, padx=5, pady=5)

        self.display_tree.column("#0", width=60, anchor=CENTER)
        self.display_tree.heading("#0", text="ID")

        self.columns = ("date", "i_code", "inv_no", "a_no", "type", "p_amt", "act")
        self.headings = ("Date", "Item Code", "Invoice No.", "Account No", "Payment Type", "Payment Amount", "Action")
        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "date":
                col_width = 100
            elif col == "i_code":
                col_width = 80
            elif col == "inv_no":
                col_width = 100
            elif col == "a_no":
                col_width = 100
            elif col == "type":
                col_width = 150
            elif col == "p_amt":
                col_width = 120
            elif col == "act":
                col_width = 150
            self.display_tree.column(col, width=col_width, anchor=CENTER)

        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    def refresh_btn_command(self):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        for data in debtor_history.display_all():
            # print(data)
            self.display_tree.insert("", END, data[0], text=data[0])
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])
            self.display_tree.set(data[0], self.columns[5], data[6])
            self.display_tree.set(data[0], self.columns[6], data[7])

    def search_command(self, event):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        if (self.search_entry.get(),) in debtor_history.i_code_check():
            for data in debtor_history.search_with_i_code(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])

        elif (self.search_entry.get(),) in debtor_history.inv_no_check():
            for data in debtor_history.search_with_inv_no(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])

        elif (self.search_entry.get(),) in debtor_history.a_no_check():
            for data in debtor_history.search_with_acc_no(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])

        elif (self.search_entry.get(),) in debtor_history.payment_type_check():
            for data in debtor_history.search_with_type(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])

        elif (self.search_entry.get(),) in debtor_history.act_check():
            for data in debtor_history.search_with_action(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])

        else:
            mbx.showinfo("", "What you entered does not exist")

    def delete_btn_command(self):
        try:
            index = self.display_tree.selection()[0]
            for data in debtor_history.select_inv_and_amt(index):
                print(data)
                if (data[0],) not in debtor.inv_no_check():
                    for elem in debtor_history.id_search(index):
                        print(elem)
                        des = i_data.get_des(elem[2])[0][0]
                        qty_rte = s_data.get_qty_and_rte(elem[3])[0]
                        print(des)
                        print(qty_rte[0])
                        print(qty_rte[1])
                        debtor.insert(
                            elem[4],
                            elem[1],
                            elem[2],
                            elem[3],
                            des,
                            qty_rte[0],
                            qty_rte[1],
                            elem[6]
                        )
                elif (data[0],) in debtor.inv_no_check():
                    debtor.part_payment_delete_reflection(
                        data[1],
                        data[0]
                    )
            debtor_history.delete(index)
            mbx.showinfo("", "Deleted successfully")

        except IndexError:
            print("IndexError: check << delete_btn_command method >>")
            pass
