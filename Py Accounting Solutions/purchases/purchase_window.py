from tkinter import *
from datetime import datetime as dt
from tkinter import ttk
from tkinter import messagebox as mbx
from purchases import purchase_data
from inventory import inventory_data
from creditors import creditors_data

c_data = creditors_data.AccountsPayableData(r"creditors_data.db")
i_data = inventory_data.InventoryDatabase(r"inventory_data.db")
t_inv = inventory_data.TrackInventoryData(r"track_inventory_data.db")
p_data = purchase_data.PurchasesData(r"purchases_database.db")
t_purchases = purchase_data.TrackPurchases(r"track_purchases_data.db")
creditor = creditors_data.AccountData(r"accounts.db")


class CreateInvoice(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Purchase Invoice")
        self.grab_set()
        # self.resizable(0, 0)
        self.frame = LabelFrame(self, text="Creditor's Details")
        self.frame.pack(fill=BOTH)
        self.frame3 = LabelFrame(self, text="Purchases Input")
        self.frame3.pack(fill=BOTH)
        self.frame2 = LabelFrame(self, text="Purchases Details")
        self.frame2.pack(fill=BOTH, expand=True)

        # ================= Customer Details ============================
        self.invoice_no = Button(self.frame, text="Invoice No.", relief=RIDGE, width=15, anchor=W,
                                 command=self.invoice_no_btn_command)
        self.invoice_no.grid(row=0, column=0, pady=5, sticky=W)
        self.invoice_no_gen = ttk.Combobox(self.frame, font=("Times New Roman", 12), state="readonly")
        self.invoice_no_gen["values"] = ["", "Creditor", "One Time"]
        self.invoice_no_gen.grid(row=0, column=1, sticky=W)
        self.invoice_no_entry = Entry(self.frame, font=("Times New Roman", 14), width=15)
        self.invoice_no_entry.grid(row=0, column=2, sticky=W, padx=5)

        # self.date_label = Label(self.frame, text="Date", anchor=W)
        # self.date_label.grid(row=0, column=3, sticky=W)
        self.date_entry = Entry(self.frame, font=("Times New Roman", 14), width=13)
        self.date_entry.insert(END, dt.today().date())
        self.date_entry.grid(row=0, column=3, sticky=W)

        self.name_label = Label(self.frame, text="Name", anchor=W)
        self.name_label.grid(row=1, column=0, sticky=W, )
        self.name_entry = Entry(self.frame, width=59, font=("Times New Roman", 12), state=DISABLED)
        self.name_entry.grid(row=1, column=1, columnspan=3, sticky=W)

        self.address_label = Label(self.frame, text="Address", anchor=W)
        self.address_label.grid(row=2, column=0, sticky=W)
        self.address_entry = Entry(self.frame, font=("Times New Roman", 12), state=DISABLED, width=22)
        self.address_entry.grid(row=2, column=1, sticky=W)

        self.location_label = Label(self.frame, text="Location", anchor=W)
        self.location_label.grid(row=3, column=0, sticky=W)
        self.location_entry = Entry(self.frame, font=("Times New Roman", 12), state=DISABLED, width=22)
        self.location_entry.grid(row=3, column=1, sticky=W)

        self.customer_no = Button(self.frame, text="Account No.", relief=RIDGE, state=DISABLED,
                                  anchor=CENTER, width=15, command=self.account_no_btn_command)
        self.customer_no.grid(row=2, column=2, sticky=W)
        self.customer_no_entry = Entry(self.frame, font=("Times New Roman", 12), state=DISABLED, width=14)
        self.customer_no_entry.grid(row=3, column=2, sticky=W, )
        self.customer_no_entry.bind("<Return>", self.account_no_btn_command_2)

        self.search = Button(self.frame, text="Search", relief=RIDGE, width=15, anchor=CENTER,
                             command=self.search_btn_command)
        self.search.grid(row=2, column=3, sticky=W)
        self.search_entry = Entry(self.frame, font=("Times New Roman", 12), width=14)
        self.search_entry.grid(row=3, column=3, sticky=W)
        self.search_entry.bind("<Return>", self.search_btn_command_2)

        # ================= SALES DATA ENTRY =============================================
        self.i_code_label = Label(self.frame3, text="Item Code", anchor=CENTER)
        self.i_code_label.grid(row=0, column=0)
        self.i_code_entry = Entry(self.frame3, width=14, justify=CENTER)
        self.i_code_entry.grid(row=1, column=0)
        self.i_code_entry.bind("<Return>", self.item_code_search_command)

        self.description_label = Label(self.frame3, text="Description", anchor=CENTER)
        self.description_label.grid(row=0, column=1)
        self.description_entry = Entry(self.frame3, width=50, justify=CENTER)
        self.description_entry.grid(row=1, column=1)

        self.quantity_label = Label(self.frame3, text="Quantity", anchor=CENTER)
        self.quantity_label.grid(row=0, column=2)
        self.quantity_entry = Entry(self.frame3, justify=CENTER)
        self.quantity_entry.grid(row=1, column=2)

        self.rate_label = Label(self.frame3, text="Rate", anchor=CENTER)
        self.rate_label.grid(row=0, column=3)
        self.rate_entry = Entry(self.frame3, justify=CENTER)
        self.rate_entry.grid(row=1, column=3)

        self.amount_label = Label(self.frame3, text="Amount", anchor=CENTER)
        self.amount_label.grid(row=0, column=4)
        self.amount_entry = Entry(self.frame3, justify=CENTER)
        self.amount_entry.grid(row=1, column=4)
        self.amount_entry.bind("<KeyPress>", self.amt_calc)

        # =============== TREEVIEW DISPLAY ===============================================
        self.display_tree = ttk.Treeview(self.frame2)
        self.display_tree.pack(anchor=N, expand=True, fill=BOTH, side=LEFT)
        self.display_tree_scroll = ttk.Scrollbar(self.frame2)
        self.display_tree_scroll.pack(anchor=N, fill=Y, side=LEFT)

        self.display_tree.config(yscrollcommand=self.display_tree_scroll.set)
        self.display_tree_scroll.config(command=self.display_tree.yview)

        self.add_new_btn = Button(self.frame2, text="Add New", relief=RIDGE, width=10,
                                  command=self.add_new_btn_command)
        self.add_new_btn.pack(anchor=N, padx=5, pady=5)

        self.update_btn = Button(self.frame2, text="Update", relief=RIDGE, width=10,
                                 command=self.update_btn_command)
        self.update_btn.pack(anchor=N, padx=5, pady=5)

        self.cancel_btn = Button(self.frame2, text="Cancel", relief=RIDGE, width=10,
                                 command=self.cancel_btn_command)
        self.cancel_btn.pack(anchor=N, padx=5, pady=5)

        self.refresh_btn = Button(self.frame2, text="Refresh", relief=RIDGE, width=10,
                                  command=self.refresh_btn_command)
        self.refresh_btn.pack(anchor=N, padx=5, pady=5)

        self.delete_btn = Button(self.frame2, text="Delete", relief=RIDGE, width=10,
                                 command=self.delete_btn_command)
        self.delete_btn.pack(anchor=N, padx=5, pady=5)

        self.close_btn = Button(self.frame2, text="Close", relief=RIDGE, width=10, command=self.destroy)
        self.close_btn.pack(anchor=N, padx=5, pady=5)

        # self.credit_btn = Button(self.frame2, text="Credit Sale", relief=RIDGE, width=10, state=DISABLED)
        # self.credit_btn.pack(anchor=N, padx=5, pady=5)
        #
        # self.cash_btn = Button(self.frame2, text="Cash Sale", relief=RIDGE, width=10, state=DISABLED)
        # self.cash_btn.pack(anchor=N, padx=5, pady=5)

        self.columns = ("date", "i_code", "invoice_no", "c_no", "name", "qty", "rte", "amt")
        self.headings = ("Date", "Item Code", "Invoice No.", "Account No.", "Name", "Quantity", "Rate", "Amount")

        self.display_tree.column("#0", width=40, anchor=CENTER)
        self.display_tree.heading("#0", text="ID")

        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "date":
                col_width = 80
            if col == "i_code":
                col_width = 70
            if col == "invoice_no":
                col_width = 80
            if col == "c_no":
                col_width = 80
            elif col == "name":
                col_width = 180
            elif col == "qty":
                col_width = 60
            elif col == "rte":
                col_width = 60
            elif col == "amt":
                col_width = 75
            self.display_tree.column(col, width=col_width, anchor=CENTER)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    #############################################################
    #              BUTTON COMMANDS
    #############################################################
    def cancel_btn_command(self):
        self.invoice_no_entry.delete(0, END)
        self.invoice_no_gen.set("")
        self.name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.location_entry.delete(0, END)
        self.customer_no_entry.delete(0, END)
        self.search_entry.delete(0, END)
        self.i_code_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.rate_entry.delete(0, END)
        self.amount_entry.delete(0, END)

    def add_new_btn_command(self):
        if (self.invoice_no_entry.get(),) in p_data.invoice_no_check():
            mbx.showinfo("Duplicate Entry Alert", "Invoice number already exist!")
        else:
            if self.invoice_no_gen.get() == "Creditor":
                if self.invoice_no_gen.get() == "" or self.invoice_no_entry.get() == "" or \
                        self.date_entry.get() == "" or self.name_entry.get() == "" or \
                        self.address_entry.get() == "" or self.location_entry.get() == "" or \
                        self.customer_no_entry.get() == "" or self.i_code_entry.get() == "" or \
                        self.description_entry.get() == "" or self.rate_entry.get() == "" or \
                        self.amount_entry.get() == "":
                    mbx.showinfo("", "Incomplete input\nPlease fill all the necessary entries")
                else:
                    i_data.update_inv_from_purchases(
                        self.i_code_entry.get(),
                        self.quantity_entry.get(),
                        self.quantity_entry.get()
                    )
                    p_data.add_new(
                        self.date_entry.get(),
                        self.name_entry.get(),
                        self.address_entry.get(),
                        self.location_entry.get(),
                        self.invoice_no_entry.get(),
                        self.customer_no_entry.get(),
                        self.i_code_entry.get(),
                        self.quantity_entry.get(),
                        self.rate_entry.get(),
                        self.amount_entry.get()
                    )
                    t_purchases.insert(
                        self.date_entry.get(),
                        self.i_code_entry.get(),
                        self.invoice_no_entry.get(),
                        self.customer_no_entry.get(),
                        self.name_entry.get(),
                        self.quantity_entry.get(),
                        self.rate_entry.get(),
                        self.amount_entry.get(),
                        user_action="New Data"
                    )
                    creditor.insert(
                        self.customer_no_entry.get(),
                        self.date_entry.get(),
                        self.i_code_entry.get(),
                        self.invoice_no_entry.get(),
                        self.description_entry.get(),
                        self.quantity_entry.get(),
                        self.rate_entry.get(),
                        self.amount_entry.get()
                    )
                    mbx.showinfo("", "Invoice created successfully")
            elif self.invoice_no_gen.get() == "One Time" and (self.i_code_entry.get(),) in i_data.search_with_code():
                if self.invoice_no_gen.get() == "One Time":
                    if self.invoice_no_gen.get() == "" or self.invoice_no_entry.get() == "" or \
                            self.date_entry.get() == "" or self.name_entry.get() == "" or \
                            self.address_entry.get() == "" or self.location_entry.get() == "" or \
                            self.description_entry.get() == "" or self.rate_entry.get() == "" or \
                            self.amount_entry.get() == "":
                        mbx.showinfo("", "Incomplete input\nPlease fill all the necessary entries")
                    else:
                        i_data.update_inv_from_purchases(
                            self.i_code_entry.get(),
                            self.quantity_entry.get(),
                            self.quantity_entry.get()
                        )
                        a_no = "One Time"
                        p_data.add_new(
                            self.date_entry.get(),
                            self.name_entry.get(),
                            self.address_entry.get(),
                            self.location_entry.get(),
                            self.invoice_no_entry.get(),
                            a_no,
                            self.i_code_entry.get(),
                            self.quantity_entry.get(),
                            self.rate_entry.get(),
                            self.amount_entry.get()
                        )
                        t_purchases.insert(
                            self.date_entry.get(),
                            self.i_code_entry.get(),
                            self.invoice_no_entry.get(),
                            a_no,
                            self.name_entry.get(),
                            self.quantity_entry.get(),
                            self.rate_entry.get(),
                            self.amount_entry.get(),
                            user_action="New Data"
                        )
                        i_n = "Default"
                        u = "Default"
                        rmk = "Default"
                        t_inv.insert(
                            i_n,
                            self.date_entry.get(),
                            self.i_code_entry.get(),
                            self.description_entry.get(),
                            u,
                            self.rate_entry.get(),
                            self.quantity_entry.get(),
                            self.amount_entry.get(),
                            rmk,
                            user_action="Purchase Data"
                        )
                        mbx.showinfo("", "Invoice created successfully")
            elif self.invoice_no_gen.get() == "One Time":
                if self.invoice_no_gen.get() == "One Time":
                    if self.invoice_no_gen.get() == "" or self.invoice_no_entry.get() == "" or \
                            self.date_entry.get() == "" or self.name_entry.get() == "" or \
                            self.address_entry.get() == "" or self.location_entry.get() == "" or \
                            self.description_entry.get() == "" or self.rate_entry.get() == "" or \
                            self.amount_entry.get() == "":
                        mbx.showinfo("", "Incomplete input\nPlease fill all the necessary entries")
                    else:
                        a_no = "One Time"
                        p_data.add_new(
                            self.date_entry.get(),
                            self.name_entry.get(),
                            self.address_entry.get(),
                            self.location_entry.get(),
                            self.invoice_no_entry.get(),
                            a_no,
                            self.i_code_entry.get(),
                            self.quantity_entry.get(),
                            self.rate_entry.get(),
                            self.amount_entry.get()
                        )
                        t_purchases.insert(
                            self.date_entry.get(),
                            self.i_code_entry.get(),
                            self.invoice_no_entry.get(),
                            a_no,
                            self.name_entry.get(),
                            self.quantity_entry.get(),
                            self.rate_entry.get(),
                            self.amount_entry.get(),
                            user_action="New Data"
                        )
                        i_c = "Default"
                        u = "Default"
                        i_data.save_btn(
                            self.date_entry.get(),
                            i_c,
                            self.description_entry.get(),
                            u,
                            self.rate_entry.get(),
                            self.quantity_entry.get(),
                            self.amount_entry.get(),
                            rmks="Default"
                        )
                        i_n = "Default"
                        i_c = "Default"
                        u = "Default"
                        rmk = "Default"
                        t_inv.insert(
                            i_n,
                            self.date_entry.get(),
                            i_c,
                            self.description_entry.get(),
                            u,
                            self.rate_entry.get(),
                            self.quantity_entry.get(),
                            self.amount_entry.get(),
                            rmk,
                            user_action="Purchase Data"
                        )
                        mbx.showinfo("", "Invoice created successfully")
            else:
                mbx.showinfo("", "Incomplete data\nPlease fill all the necessary entries")

    def update_btn_command(self):
        if self.customer_no_entry.get() == "" or self.i_code_entry.get() == "" or \
                self.quantity_entry.get() == "" or self.rate_entry.get() == "" or \
                self.amount_entry.get() == "":
            mbx.showinfo("Incomplete Data Alert", "Incomplete data input\nPlease fill all the necessary entries")
        else:
            for data in p_data.update_reflection(self.invoice_no_entry.get()):
                print(data)
                actual_qty = data[0]
                updated_qty = float(self.quantity_entry.get())
                revised_qty = updated_qty - actual_qty
                i_data.reflection_from_update(self.i_code_entry.get(), revised_qty, revised_qty)
            p_data.update(
                self.invoice_no_entry.get(),
                self.name_entry.get(),
                self.address_entry.get(),
                self.location_entry.get(),
                self.customer_no_entry.get(),
                self.i_code_entry.get(),
                self.quantity_entry.get(),
                self.rate_entry.get(),
                self.amount_entry.get()
            )
            t_purchases.insert(
                self.date_entry.get(),
                self.i_code_entry.get(),
                self.invoice_no_entry.get(),
                self.customer_no_entry.get(),
                self.name_entry.get(),
                self.quantity_entry.get(),
                self.rate_entry.get(),
                self.amount_entry.get(),
                user_action="Updated Data"
            )
            i_n = ""
            u = ""
            t_inv.insert(
                i_n,
                self.date_entry.get(),
                self.i_code_entry.get(),
                self.description_entry.get(),
                u,
                self.rate_entry.get(),
                self.quantity_entry.get(),
                self.amount_entry.get(),
                self.name_entry.get(),
                user_action="Purchase Update"
            )
            creditor.update(
                self.i_code_entry.get(),
                self.description_entry.get(),
                self.quantity_entry.get(),
                self.rate_entry.get(),
                self.amount_entry.get(),
                self.invoice_no_entry.get()
            )
            mbx.showinfo("Updated Alert", "Invoice updated successfully")

    def delete_btn_command(self):
        try:
            index = self.display_tree.selection()
            print(index[0])
            if len(str(index[0])) > 0:
                query = mbx.askyesno("Confirm Delete", "Do you want to delete the selected invoice?")
                if query is True:
                    for data in p_data.track_deleted_data_by_id(index[0]):
                        print(data)
                        del_data = float(data[8])
                        i_c = data[7]
                        i_data.purchase_deletion_reflection(i_c, del_data, del_data)
                        t_purchases.insert(
                            data[1],
                            data[7],
                            data[5],
                            data[6],
                            data[2],
                            data[8],
                            data[9],
                            data[10],
                            user_action="Deleted Data"
                        )
                        creditor.delete(data[5])
                    p_data.delete_with_id(index[0])
                    mbx.showinfo("", "Deleted Successfully")
        except IndexError:
            if self.invoice_no_entry.get() == "":
                mbx.showinfo("", "Invoice number entry is empty\nPlease enter invoice number to be deleted")
            elif self.invoice_no_entry.get() != "":
                query = mbx.askyesno("Confirm Delete", "Do you want to delete the selected invoice?")
                if query is True:
                    del_data2 = float(self.quantity_entry.get())
                    i_data.purchase_deletion_reflection(self.i_code_entry.get(), del_data2, del_data2)
                    t_purchases.insert(
                        self.date_entry.get(),
                        self.i_code_entry.get(),
                        self.invoice_no_entry.get(),
                        self.customer_no_entry.get(),
                        self.name_entry.get(),
                        self.quantity_entry.get(),
                        self.rate_entry.get(),
                        self.amount_entry.get(),
                        user_action="Deleted Data"
                    )
                    creditor.delete(self.invoice_no_entry.get())
                    p_data.delete_with_invoice_no(self.invoice_no_entry.get())
                    mbx.showinfo("", "Deleted Successfully")
            else:
                mbx.showinfo("", "You have not selected anything")

    def refresh_btn_command(self):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        try:
            self.customer_no.config(state=DISABLED)
            self.customer_no_entry.config(state=DISABLED)
            self.name_entry.config(state=DISABLED)
            self.address_entry.config(state=DISABLED)
            self.location_entry.config(state=DISABLED)
            for data in p_data.display_all():
                print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[2])
                self.display_tree.set(data[0], self.columns[1], data[1])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])
                self.display_tree.set(data[0], self.columns[7], data[8])
        except Exception:
            pass

    def invoice_no_btn_command(self):
        try:
            self.invoice_no_entry.delete(0, END)
            length = str(p_data.invoice_no_gen()[0][0])
            num = p_data.invoice_no_gen()[0][0] + 1
            # INVOICE NUMBER FOR CREDITORS
            if len(length) == 1 and self.invoice_no_gen.get() == "Creditor":
                i_n = "CPUR" + "000" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.customer_no.config(state=NORMAL)
                self.customer_no_entry.config(state=NORMAL)
                self.name_entry.config(state=DISABLED)
                self.address_entry.config(state=DISABLED)
                self.location_entry.config(state=DISABLED)
            elif len(length) == 2 and self.invoice_no_gen.get() == "Creditor":
                i_n = "CPUR" + "00" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.customer_no.config(state=NORMAL)
                self.customer_no_entry.config(state=NORMAL)
                self.name_entry.config(state=DISABLED)
                self.address_entry.config(state=DISABLED)
                self.location_entry.config(state=DISABLED)
            elif len(length) == 3 and self.invoice_no_gen.get() == "Creditor":
                i_n = "CPUR" + "0" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.customer_no.config(state=NORMAL)
                self.customer_no_entry.config(state=NORMAL)
                self.name_entry.config(state=DISABLED)
                self.address_entry.config(state=DISABLED)
                self.location_entry.config(state=DISABLED)
            elif len(length) >= 4 and self.invoice_no_gen.get() == "Creditor":
                i_n = "CPUR" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.customer_no.config(state=NORMAL)
                self.customer_no_entry.config(state=NORMAL)
                self.name_entry.config(state=DISABLED)
                self.address_entry.config(state=DISABLED)
                self.location_entry.config(state=DISABLED)
            # INVOICE NUMBER FOR ONE TIME PURCHASE
            elif len(length) == 1 and self.invoice_no_gen.get() == "One Time":
                i_n = "OPUR" + "000" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.name_entry.config(state=NORMAL)
                self.address_entry.config(state=NORMAL)
                self.location_entry.config(state=NORMAL)
                self.customer_no.config(state=DISABLED)
                self.customer_no_entry.config(state=DISABLED)
            elif len(length) == 2 and self.invoice_no_gen.get() == "One Time":
                i_n = "OPUR" + "00" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.name_entry.config(state=NORMAL)
                self.address_entry.config(state=NORMAL)
                self.location_entry.config(state=NORMAL)
                self.customer_no.config(state=DISABLED)
                self.customer_no_entry.config(state=DISABLED)
            elif len(length) == 3 and self.invoice_no_gen.get() == "One Time":
                i_n = "OPUR" + "0" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.name_entry.config(state=NORMAL)
                self.address_entry.config(state=NORMAL)
                self.location_entry.config(state=NORMAL)
                self.customer_no.config(state=DISABLED)
                self.customer_no_entry.config(state=DISABLED)
            elif len(length) >= 4 and self.invoice_no_gen.get() == "One Time":
                i_n = "OPUR" + str(num)
                self.invoice_no_entry.insert(END, i_n)
                self.name_entry.config(state=NORMAL)
                self.address_entry.config(state=NORMAL)
                self.location_entry.config(state=NORMAL)
                self.customer_no.config(state=DISABLED)
                self.customer_no_entry.config(state=DISABLED)
        except IndexError:
            if self.invoice_no_gen.get() == "Creditor":
                self.invoice_no_entry.insert(END, "CPUR0001")
                self.customer_no.config(state=NORMAL)
                self.customer_no_entry.config(state=NORMAL)
                self.name_entry.config(state=DISABLED)
                self.address_entry.config(state=DISABLED)
                self.location_entry.config(state=DISABLED)
            elif self.invoice_no_gen.get() == "One Time":
                self.invoice_no_entry.insert(END, "OPUR0001")
                self.name_entry.config(state=NORMAL)
                self.address_entry.config(state=NORMAL)
                self.location_entry.config(state=NORMAL)
                self.customer_no.config(state=DISABLED)
                self.customer_no_entry.config(state=DISABLED)

    def search_btn_command(self):
        if (self.search_entry.get(),) in p_data.invoice_no_check():
            self.name_entry.config(state=NORMAL)
            self.address_entry.config(state=NORMAL)
            self.location_entry.config(state=NORMAL)
            self.customer_no.config(state=NORMAL)
            self.customer_no_entry.config(state=NORMAL)
            try:
                self.name_entry.delete(0, END)
                self.address_entry.delete(0, END)
                self.location_entry.delete(0, END)
                self.invoice_no_entry.delete(0, END)
                self.customer_no_entry.delete(0, END)
                self.i_code_entry.delete(0, END)
                self.description_entry.delete(0, END)
                self.quantity_entry.delete(0, END)
                self.rate_entry.delete(0, END)
                self.amount_entry.delete(0, END)
                for data in p_data.search_invoice(self.search_entry.get()):
                    print(data)
                    self.name_entry.insert(END, data[2])
                    self.address_entry.insert(END, data[3])
                    self.location_entry.insert(END, data[4])
                    self.invoice_no_entry.insert(END, data[5])
                    self.customer_no_entry.insert(END, data[6])
                    self.i_code_entry.insert(END, data[7])
                    self.quantity_entry.insert(END, data[8])
                    self.rate_entry.insert(END, data[9])
                    self.amount_entry.insert(END, data[10])
                    for inv in i_data.sales_entry(data[7]):
                        self.description_entry.insert(END, inv[1])
            except IndexError:
                pass
        else:
            mbx.showinfo("", "Invoice number does not exist")

    def search_btn_command_2(self, event):
        if (self.search_entry.get(),) in p_data.invoice_no_check():
            self.name_entry.config(state=NORMAL)
            self.address_entry.config(state=NORMAL)
            self.location_entry.config(state=NORMAL)
            self.customer_no.config(state=NORMAL)
            self.customer_no_entry.config(state=NORMAL)
            try:
                self.name_entry.delete(0, END)
                self.address_entry.delete(0, END)
                self.location_entry.delete(0, END)
                self.invoice_no_entry.delete(0, END)
                self.customer_no_entry.delete(0, END)
                self.i_code_entry.delete(0, END)
                self.description_entry.delete(0, END)
                self.quantity_entry.delete(0, END)
                self.rate_entry.delete(0, END)
                self.amount_entry.delete(0, END)
                for data in p_data.search_invoice(self.search_entry.get()):
                    print(data)
                    self.name_entry.insert(END, data[2])
                    self.address_entry.insert(END, data[3])
                    self.location_entry.insert(END, data[4])
                    self.invoice_no_entry.insert(END, data[5])
                    self.customer_no_entry.insert(END, data[6])
                    self.i_code_entry.insert(END, data[7])
                    self.quantity_entry.insert(END, data[8])
                    self.rate_entry.insert(END, data[9])
                    self.amount_entry.insert(END, data[10])
                    for inv in i_data.sales_entry(data[7]):
                        self.description_entry.insert(END, inv[1])
            except IndexError:
                pass
        else:
            mbx.showinfo("", "Invoice number does not exist")

    def item_code_search_command(self, event):
        if (self.i_code_entry.get(),) in i_data.item_code_check():
            self.description_entry.delete(0, END)
            self.quantity_entry.delete(0, END)
            self.rate_entry.delete(0, END)
            self.amount_entry.delete(0, END)
            i_data.sales_entry(self.i_code_entry.get())
            for data in i_data.sales_entry(self.i_code_entry.get()):
                self.description_entry.insert(END, data[1])
                self.rate_entry.insert(END, data[2])
        else:
            mbx.showinfo("", "Item code does not exist")

    def account_no_btn_command(self):
        try:
            if (self.customer_no_entry.get(),) in c_data.account_no_check():
                self.name_entry.config(state=NORMAL)
                self.address_entry.config(state=NORMAL)
                self.location_entry.config(state=NORMAL)
                self.name_entry.delete(0, END)
                self.address_entry.delete(0, END)
                self.location_entry.delete(0, END)
                for data in c_data.search_with_account_no(self.customer_no_entry.get()):
                    name = data[0:2]
                    address = data[2]
                    location = data[3]
                    self.name_entry.insert(END, name)
                    self.address_entry.insert(END, address)
                    self.location_entry.insert(END, location)
            else:
                mbx.showinfo("", "Customer number does not exist")
        except IndexError:
            mbx.showinfo("", "Customer database is empty")

    def account_no_btn_command_2(self, event):
        try:
            if (self.customer_no_entry.get(),) in c_data.account_no_check():
                self.name_entry.config(state=NORMAL)
                self.address_entry.config(state=NORMAL)
                self.location_entry.config(state=NORMAL)
                self.name_entry.delete(0, END)
                self.address_entry.delete(0, END)
                self.location_entry.delete(0, END)
                for data in c_data.search_with_account_no(self.customer_no_entry.get()):
                    name = data[0:2]
                    address = data[2]
                    location = data[3]
                    self.name_entry.insert(END, name)
                    self.address_entry.insert(END, address)
                    self.location_entry.insert(END, location)
            else:
                mbx.showinfo("", "Customer number does not exist")
        except IndexError:
            mbx.showinfo("", "Customer database is empty")

    def amt_calc(self, event):
        self.amount_entry.delete(0, END)
        rte = float(self.rate_entry.get())
        qty = float(self.quantity_entry.get())
        amt = rte * qty
        self.amount_entry.insert(END, amt)


class TrackPurchases(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Track Purchases")
        self.grab_set()
        self.search = Label(self, text="Search", font=("Times New Roman", 13))
        self.search.pack()
        self.search_entry = Entry(self, width=40)
        self.search_entry.pack()
        self.search_entry.bind("<Return>", self.search_command)
        self.columns = ("date", "i_code", "inv_no", "c_no", "name", "qty", "rte", "amt", "action")
        self.headings = (
            "Date", "Item Code", "Invoice No.", "Customer No.", "Name", "Quantity", "Rate", "Amount", "Action")
        self.display_tree = ttk.Treeview(self)
        self.display_tree.pack(expand=True, fill=BOTH, side=LEFT)
        self.display_tree_scroll = ttk.Scrollbar(self)
        self.display_tree_scroll.pack(side=LEFT, fill=Y)
        self.display_tree_scroll.config(command=self.display_tree.yview)
        self.refresh_btn = Button(self, text="Refresh", width=15, relief=RIDGE,
                                  command=self.refresh_btn_command)
        self.refresh_btn.pack(side=LEFT, anchor=N, padx=5, pady=5)
        self.display_tree.column("#0", width=60, anchor=CENTER)
        self.display_tree.heading("#0", text="ID")
        self.display_tree.config(columns=self.columns, yscrollcommand=self.display_tree_scroll.set)
        for col in self.columns:
            if col == "date":
                col_width = 80
            elif col == "i_code":
                col_width = 100
            elif col == "inv_no":
                col_width = 100
            elif col == "c_no":
                col_width = 100
            elif col == "name":
                col_width = 350
            elif col == "qty":
                col_width = 80
            elif col == "rte":
                col_width = 80
            elif col == "amt":
                col_width = 100
            elif col == "action":
                col_width = 100
            self.display_tree.column(col, width=col_width, anchor=CENTER)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1

    def refresh_btn_command(self):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        for data in t_purchases.display_all():
            # print(data)
            self.display_tree.insert("", END, data[0], text=data[0])
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])
            self.display_tree.set(data[0], self.columns[5], data[6])
            self.display_tree.set(data[0], self.columns[6], data[7])
            self.display_tree.set(data[0], self.columns[7], data[8])
            self.display_tree.set(data[0], self.columns[8], data[9])

    def search_command(self, event):
        if self.search_entry.get() == "":
            mbx.showinfo("", "You have not entered anything")
        elif (self.search_entry.get(),) in t_purchases.account_no_check():
            for children in self.display_tree.get_children():
                self.display_tree.delete(children)
            for data in t_purchases.search_with_account_no(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])
                self.display_tree.set(data[0], self.columns[7], data[8])
                self.display_tree.set(data[0], self.columns[8], data[9])
        elif (self.search_entry.get(),) in t_purchases.item_code_check():
            for children in self.display_tree.get_children():
                self.display_tree.delete(children)
            for data in t_purchases.search_with_item_code(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])
                self.display_tree.set(data[0], self.columns[7], data[8])
                self.display_tree.set(data[0], self.columns[8], data[9])
        elif (self.search_entry.get(),) in t_purchases.inv_no_check():
            for children in self.display_tree.get_children():
                self.display_tree.delete(children)
            for data in t_purchases.search_with_invoice_no(self.search_entry.get()):
                # print(data)
                self.display_tree.insert("", END, data[0], text=data[0])
                self.display_tree.set(data[0], self.columns[0], data[1])
                self.display_tree.set(data[0], self.columns[1], data[2])
                self.display_tree.set(data[0], self.columns[2], data[3])
                self.display_tree.set(data[0], self.columns[3], data[4])
                self.display_tree.set(data[0], self.columns[4], data[5])
                self.display_tree.set(data[0], self.columns[5], data[6])
                self.display_tree.set(data[0], self.columns[6], data[7])
                self.display_tree.set(data[0], self.columns[7], data[8])
                self.display_tree.set(data[0], self.columns[8], data[9])
        else:
            mbx.showinfo("", "What you entered does not exist")
