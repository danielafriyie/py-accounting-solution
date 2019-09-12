"""
Inventory window
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbx
from datetime import datetime as dt
from inventory import inventory_data

i_data = inventory_data.InventoryDatabase(r"inventory_data.db")
t_inv = inventory_data.TrackInventoryData(r"track_inventory_data.db")


class InventoryInput(Toplevel):
    """
        Inventory Data Entry
            * Add new inventory
            * Update inventory
            * Delete inventory
    """

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Inventory Data")
        self.config(background="light blue")
        self.grab_set()

        # self.frame = Frame(self).pack()

        self.data_input_frame_box = LabelFrame(self, text="Select Item")
        self.data_input_frame_box.pack(side=LEFT, anchor=N, fill=BOTH)

        self.data_input_frame = LabelFrame(self, text="Item Entry")
        self.data_input_frame.pack(anchor=N, fill=BOTH)

        self.details_box_frame = LabelFrame(self, text="Item Description")
        self.details_box_frame.pack(side=BOTTOM, expand=True, fill=BOTH)

        self.details_btn_frame = Frame(self)
        self.details_btn_frame.pack()

        # ============= Items Code Box with Search Entry ===================
        self.search = Entry(self.data_input_frame_box, width=23)
        self.search.pack()
        self.search.bind("<Return>", self.search_command)

        self.items_code_box = Listbox(self.data_input_frame_box, )
        self.items_code_box.pack(side=LEFT, anchor=N, expand=True, fill=Y)
        self.items_code_box.bind('<<ListboxSelect>>', self.selected_data)

        ###########################################
        # INSERT ITEM CODE INTO self.item_code_box
        ###########################################
        for code in i_data.display_item_code():
            # self.items_code_box.delete(0, END)
            self.items_code_box.insert(END, code[0])

        self.items_code_box_scrollbar = ttk.Scrollbar(self.data_input_frame_box)
        self.items_code_box.configure(yscrollcommand=self.items_code_box_scrollbar.set)
        self.items_code_box_scrollbar.configure(command=self.items_code_box.yview)
        self.items_code_box_scrollbar.pack(fill=Y, side=RIGHT, anchor=N)

        # ==================== Items entry ========================
        self.date_label = Label(self.data_input_frame, text="Date")
        self.date_label.grid(row=0, column=0, sticky=W)
        self.date_entry = Entry(self.data_input_frame, )
        self.date_entry.grid(row=0, column=1, sticky=W)

        self.item_code_label = Label(self.data_input_frame, text="Item Code")
        self.item_code_label.grid(row=1, column=0, sticky=W)
        self.item_code_entry = Entry(self.data_input_frame)
        self.item_code_entry.grid(row=1, column=1, sticky=W)

        self.description_label = Label(self.data_input_frame, text="Description")
        self.description_label.grid(row=2, column=0, sticky=W)
        self.description_entry = Entry(self.data_input_frame, width=50)
        self.description_entry.grid(row=2, column=1, sticky=W)

        self.unit_label = Label(self.data_input_frame, text="Unit")
        self.unit_label.grid(row=3, column=0, sticky=W)
        self.unit_entry = Entry(self.data_input_frame, )
        self.unit_entry.grid(row=3, column=1, sticky=W)

        self.rate_label = Label(self.data_input_frame, text="Rate")
        self.rate_label.grid(row=4, column=0, sticky=W)
        self.rate_entry = Entry(self.data_input_frame)
        self.rate_entry.grid(row=4, column=1, sticky=W)

        self.qty_label = Label(self.data_input_frame, text="Quantity")
        self.qty_label.grid(row=5, column=0, sticky=W)
        self.qty_entry = Entry(self.data_input_frame, )
        self.qty_entry.grid(row=5, column=1, sticky=W)

        self.amount_label = Label(self.data_input_frame, text="Amount")
        self.amount_label.grid(row=6, column=0, sticky=W)
        self.amount_entry = Entry(self.data_input_frame)
        self.amount_entry.bind("<KeyPress>", self.amt_calc)
        self.amount_entry.grid(row=6, column=1, sticky=W)

        self.remarks_label = Label(self.data_input_frame, text="Remarks")
        self.remarks_label.grid(row=7, column=0, sticky=W)
        self.remarks_entry = Entry(self.data_input_frame, width=50)
        self.remarks_entry.grid(row=7, column=1, sticky=W)

        # ================= Item Description ==========================
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
        self.columns = ('date', 'i_code', 'des', 'unit', 'rte', 'qty', 'amt', 'rmks')
        self.headings = ('Date', 'Item Code', 'Description', 'Unit', 'Rate', 'Quantity', 'Amount', 'Remarks')
        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == 'date':
                col_width = 75
            elif col == "i_code":
                col_width = 85
            elif col == "des":
                col_width = 250
            elif col == "unit":
                col_width = 45
            elif col == "rte":
                col_width = 50
            elif col == 'qty':
                col_width = 75
            elif col == "amt":
                col_width = 80
            elif col == "rmks":
                col_width = 250

            self.display_tree.column(col, width=col_width, anchor=CENTER)
        counter = 0
        for col in self.columns:
            self.display_tree.heading(col, text=self.headings[counter])
            counter += 1
        self.display_tree.column('#0', width=80)
        self.display_tree.heading("#0", text="Item No.")

        ######################################################
        # BUTTON COMMANDS AND INTERACTIONS TO THE DATABASE
        ######################################################
        """ Inserts the current date to the date entry column """
        self.current_date = dt.today()
        self.date_entry.delete(0, END)
        self.date_entry.insert(END, self.current_date.date())

    def amt_calc(self, event):
        """ Amount Calculation """
        self.amount_entry.delete(0, END)
        try:
            amt = float(self.rate_entry.get()) * float(self.qty_entry.get())
            self.amount_entry.insert(END, amt)
        except ValueError:
            print("ValueError, Check rate and quantity entries to see if it's values can"
                  " be converted to float")
            pass

    def save_btn_command(self):
        try:
            # check to see if all the necessary entries are filled
            if self.item_code_entry.get() == '' or self.description_entry.get() == '' or \
                    self.unit_entry.get() == '' or self.rate_entry.get() == '' or \
                    self.qty_entry.get() == '' or self.remarks_entry.get() == '' or self.amount_entry.get() == '':
                mbx.showinfo("Incomplete data alert", "Incomplete Input\nPlease fill all the necessary entries")
            elif (self.item_code_entry.get(),) in i_data.search_with_code():
                mbx.showinfo("Duplicate Alert", "Item Code already exist")
            else:
                i_data.save_btn(
                    self.date_entry.get(),
                    self.item_code_entry.get(),
                    self.description_entry.get(),
                    self.unit_entry.get(),
                    self.rate_entry.get(),
                    self.qty_entry.get(),
                    self.amount_entry.get(),
                    self.remarks_entry.get()
                )
                # INSERTS DATA INTO TRACKING DATABASE
                action = "New Data"
                item_no_generation = int(i_data.item_no_select()[0][0])
                t_inv.insert(
                    item_no_generation,
                    self.date_entry.get(),
                    self.item_code_entry.get(),
                    self.description_entry.get(),
                    self.unit_entry.get(),
                    self.rate_entry.get(),
                    self.qty_entry.get(),
                    self.amount_entry.get(),
                    self.remarks_entry.get(),
                    action
                )
                mbx.showinfo("Saved alert", "Saved Successfully")
        except IndexError:
            print("There is an IndexError: empty database")
            pass

    def cancel_btn_command(self):
        # self.date_entry.delete(0, END)
        self.item_code_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.unit_entry.delete(0, END)
        self.rate_entry.delete(0, END)
        self.qty_entry.delete(0, END)
        self.remarks_entry.delete(0, END)
        self.amount_entry.delete(0, END)

    def refresh_btn_command(self):
        self.items_code_box.delete(0, END)
        for elements in self.display_tree.get_children():
            self.display_tree.delete(elements)
        for data in i_data.display_data():
            self.display_tree.insert('', END, data[0], text=data[0])
            self.columns = ('date', 'i_code', 'des', 'unit', 'rte', 'qty', 'amt', 'rmks')
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])
            self.display_tree.set(data[0], self.columns[5], data[6])
            self.display_tree.set(data[0], self.columns[6], data[7])
            self.display_tree.set(data[0], self.columns[7], data[8])

        # INSERTS ITEMS CODE INTO ITEMS CODE BOX
        for code in i_data.display_item_code():
            for elem in code:
                self.items_code_box.insert(END, elem)

    def delete_btn_command(self):
        try:
            # prompts the user to confirm delete
            query = mbx.askyesno("Confirm Delete", "Do you want to delete the selected data")
            if query is True:
                index = self.display_tree.selection()

                # INSERTS DATA INTO TRACKING DATABASE BEFORE DELETE TAKES PLACE
                action = "Deleted Data"
                item_no_generation = index[0]
                for track in i_data.edit_btn(index[0]):
                    t_inv.insert(
                        item_no_generation,
                        self.date_entry.get(),
                        track[2],
                        track[3],
                        track[4],
                        track[5],
                        track[6],
                        track[7],
                        track[8],
                        action
                    )
                i_data.delete_btn(index[0])
                mbx.showinfo("Deleted alert", "Deleted Successfully")
        except IndexError:  # Check for IndexError
            print("There is an IndexError: 'index' variable is empty")
            mbx.showinfo("Nothing Selected Alert", "You have not selected anything")

    def edit_btn_command(self):
        index = self.display_tree.selection()
        self.item_code_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.unit_entry.delete(0, END)
        self.rate_entry.delete(0, END)
        self.qty_entry.delete(0, END)
        self.remarks_entry.delete(0, END)
        self.amount_entry.delete(0, END)
        try:
            for data in i_data.edit_btn(index[0]):
                self.item_code_entry.insert(END, data[2])
                self.description_entry.insert(END, data[3])
                self.unit_entry.insert(END, data[4])
                self.rate_entry.insert(END, data[5])
                self.qty_entry.insert(END, data[6])
                self.amount_entry.insert(END, data[7])
                self.remarks_entry.insert(END, data[8])
        except IndexError:
            print("There is an IndexError: 'index' variable is empty")
            mbx.showinfo("Nothing Selected Alert", "You have not selected anything")

    def update_btn_command(self):
        action = "Updated Data"
        try:
            index = self.display_tree.selection()
            if self.item_code_entry.get() == '' or self.description_entry.get() == '' or \
                    self.unit_entry.get() == '' or self.rate_entry.get() == '' or \
                    self.qty_entry.get() == '' or self.remarks_entry.get() == '':
                mbx.showinfo("Incomplete Data Alert", "Incomplete Input\nPlease fill all the necessary entries")
            else:
                i_data.update_btn(
                    index[0],
                    self.date_entry.get(),
                    self.item_code_entry.get(),
                    self.description_entry.get(),
                    self.unit_entry.get(),
                    self.rate_entry.get(),
                    self.qty_entry.get(),
                    self.amount_entry.get(),
                    self.remarks_entry.get()
                )
                # INSERTS DATA INTO TRACKING DATABASE
                item_no_generation = index[0]
                t_inv.insert(
                    item_no_generation,
                    self.date_entry.get(),
                    self.item_code_entry.get(),
                    self.description_entry.get(),
                    self.unit_entry.get(),
                    self.rate_entry.get(),
                    self.qty_entry.get(),
                    self.amount_entry.get(),
                    self.remarks_entry.get(),
                    action
                )
                mbx.showinfo("Update Alert", "Updated Successfully")
        except IndexError:
            mbx.showinfo("Update Error Alert", "Use edit to select data before updating it")
            print("There is an IndexError: use edit button to select data before updating it")
            pass

    def selected_data(self, event):
        try:
            index = self.items_code_box.curselection()[0]
            selected_row = self.items_code_box.get(index)
            data = i_data.get_selected_row(selected_row)
            self.item_code_entry.delete(0, END)
            self.item_code_entry.insert(END, data[0][2])
            self.description_entry.delete(0, END)
            self.description_entry.insert(END, data[0][3])
            self.unit_entry.delete(0, END)
            self.unit_entry.insert(END, data[0][4])
            self.rate_entry.delete(0, END)
            self.rate_entry.insert(END, data[0][5])
            self.qty_entry.delete(0, END)
            self.qty_entry.insert(END, data[0][6])
            self.amount_entry.delete(0, END)
            self.amount_entry.insert(END, data[0][7])
            self.remarks_entry.delete(0, END)
            self.remarks_entry.insert(END, data[0][8])
        except IndexError:
            print("There us an IndexError: 'self.item_code_box' is empty")
            pass

    def search_command(self, event):
        for code in i_data.search_with_code():
            if self.search.get() in code:
                self.items_code_box.delete(0, END)
                self.items_code_box.insert(END, self.search.get())


class TrackInventory(Toplevel):
    """
        Inventory Tracking
            * Track new entries
            * Track deleted entries
            * Track updated entries
    """

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Inventory Tracking")
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

        self.refresh_btn = Button(self, text="Refresh", width=15, relief=RIDGE, command=self.refresh_btn_command)
        self.refresh_btn.pack(side=LEFT, anchor=N, padx=5, pady=5)

        # COLUMN AND HEADING NAMES FOR THE TREEVIEW
        self.columns = ("item_no", "date", "i_code", "des", "unit", "rte", "qty", "amt", "rmks", "action")
        self.headings = (
            "Item No.", "Date", "Item code", "Description", "Unit", "Rate", "Quantity", "Amount", "Remarks", "Action")

        self.display_tree.heading("#0", text="ID")
        self.display_tree.column("#0", width=55)

        self.display_tree.config(columns=self.columns)
        for col in self.columns:
            if col == "item_no":
                col_width = 55
            elif col == "date":
                col_width = 80
            elif col == "i_code":
                col_width = 80
            elif col == "des":
                col_width = 250
            elif col == "unit":
                col_width = 55
            elif col == "rte":
                col_width = 55
            elif col == "qty":
                col_width = 55
            elif col == "amt":
                col_width = 85
            elif col == "rmks":
                col_width = 250
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
        for data in t_inv.display():
            self.display_tree.insert('', END, data[0], text=data[0])
            self.display_tree.set(data[0], self.columns[0], data[1])
            self.display_tree.set(data[0], self.columns[1], data[2])
            self.display_tree.set(data[0], self.columns[2], data[3])
            self.display_tree.set(data[0], self.columns[3], data[4])
            self.display_tree.set(data[0], self.columns[4], data[5])
            self.display_tree.set(data[0], self.columns[5], data[6])
            self.display_tree.set(data[0], self.columns[6], data[7])
            self.display_tree.set(data[0], self.columns[7], data[8])
            self.display_tree.set(data[0], self.columns[8], data[9])
            self.display_tree.set(data[0], self.columns[9], data[10])

    def search_command(self, event):
        for children in self.display_tree.get_children():
            self.display_tree.delete(children)
        if (self.search_entry.get(),) in t_inv.item_code_check():
            for elem in t_inv.search_with_item_code(self.search_entry.get()):
                self.display_tree.insert('', END, elem[0], text=elem[0])
                self.display_tree.set(elem[0], self.columns[0], elem[1])
                self.display_tree.set(elem[0], self.columns[1], elem[2])
                self.display_tree.set(elem[0], self.columns[2], elem[3])
                self.display_tree.set(elem[0], self.columns[3], elem[4])
                self.display_tree.set(elem[0], self.columns[4], elem[5])
                self.display_tree.set(elem[0], self.columns[5], elem[6])
                self.display_tree.set(elem[0], self.columns[6], elem[7])
                self.display_tree.set(elem[0], self.columns[7], elem[8])
                self.display_tree.set(elem[0], self.columns[8], elem[9])
                self.display_tree.set(elem[0], self.columns[9], elem[10])
        elif (self.search_entry.get(),) in t_inv.action_check():
            for elem in t_inv.search_with_action(self.search_entry.get()):
                self.display_tree.insert('', END, elem[0], text=elem[0])
                self.display_tree.set(elem[0], self.columns[0], elem[1])
                self.display_tree.set(elem[0], self.columns[1], elem[2])
                self.display_tree.set(elem[0], self.columns[2], elem[3])
                self.display_tree.set(elem[0], self.columns[3], elem[4])
                self.display_tree.set(elem[0], self.columns[4], elem[5])
                self.display_tree.set(elem[0], self.columns[5], elem[6])
                self.display_tree.set(elem[0], self.columns[6], elem[7])
                self.display_tree.set(elem[0], self.columns[7], elem[8])
                self.display_tree.set(elem[0], self.columns[8], elem[9])
                self.display_tree.set(elem[0], self.columns[9], elem[10])
        else:
            mbx.showinfo("", "What you entered does not exist")
