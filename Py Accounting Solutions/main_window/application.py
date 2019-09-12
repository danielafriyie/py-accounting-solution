"""
    Main Application interface
"""

__app_name__ = "Py Accounting Solutions"
__version__ = "1.0"
__author__ = "Afriyie Daniel"
__email__ = "afriyiedaniel1@outlook.com"
__status__ = "Development"
__description__ = "A simple accounting solution program"

from tkinter import *
import tkinter.messagebox as mbx
from inventory import inventory_window, inventory_data
from debtors import debtors_window, debtors_data
from creditors import creditors_data, creditors_window
from sales import sales_window, sales_data
from purchases import purchase_data, purchase_window
from expenditure import expenditure_window, expenditure_data
from reports import expense_report, inventory_report, sales_report, purchase_report
from reports import accounts_receivable_report, accounts_payable_report, profit_or_loss_report

# ================= Inventory Data ====================================================
i_data = inventory_data.InventoryDatabase(r"inventory_data.db")
t_inv = inventory_data.TrackInventoryData(r"track_inventory_data.db")

# ==================== Debtors Data ==================================================
d_data = debtors_data.AccountsReceivableData(r"debtors_data.db")
t_debtors = debtors_data.TrackDebtorsData(r"track_debtors.db")
debtor = debtors_data.AccountData(r"accounts.db")
debtor_history = debtors_data.AccountHistory(r"account_history.db")

# ====================== Creditors Data ==============================================
c_data = creditors_data.AccountsPayableData(r"creditors_data.db")
t_creditors = creditors_data.TrackCreditorsData(r"track_creditors.db")
creditor = creditors_data.AccountData(r"accounts.db")
creditor_history = creditors_data.AccountHistory(r"account_history.db")

# ========================== Sales Data =============================================
s_data = sales_data.SalesData(r"sales_database.db")
t_sales = sales_data.TrackSales(r"track_sales_data.db")

# ============================ Purchases Data ============================
p_data = purchase_data.PurchasesData(r"purchases_database.db")
t_purchases = purchase_data.TrackPurchases(r"track_purchases_data.db")

# ============================ Expenses Data ====================================
e_data = expenditure_data.ExpensesData(r"exp_data.db")
t_expenses = expenditure_data.TrackExpenditure(r"tack_exp_data.db")


class MainWindow(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master.title(" " + __app_name__ + " " + __version__)
        self.master.geometry("+100+100")
        self.master.resizable(0, 0)
        self.master.protocol('WM_DELETE_WINDOW', self.exit_command)
        self.master.iconbitmap(default="main.ico")
        # self.master.iconbitmap("images\\main.ico")
        self.master.configure(background="light green")
        self.image = PhotoImage(file=r"background.png")
        self.background_image = Label(self.master, image=self.image)
        self.background_image.image = self.image
        self.background_image.pack(fill='both', expand=True)
        # self.master.grab_release()
        self.pack(fill=BOTH, expand=True)

        #################################################
        # Add drop down menu to the main window(master)
        ################################################
        self.drop_down_menus = Menu(self.master)
        self.master.config(menu=self.drop_down_menus)

        """
                      DROP DOWN MENU COMMANDS
        """

        # ******************** Inventory *****************
        self.inventory = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Inventory", menu=self.inventory)
        self.inventory.add_command(label="Data Entry", command=self.inventory_input)
        # self.inventory.add_command(label="Inventory Items")
        self.inventory.add_separator()
        self.inventory.add_command(label="Track Inventory", command=self.inventory_tracking)

        # ************** Debtors ***************************
        self.debtors = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Accounts Receivable", menu=self.debtors)
        self.debtors.add_command(label="Accounts", command=self.accounts_receivable)
        # self.debtors.add_command(label="Update Account")
        # self.debtors.add_command(label="Debtors List")
        self.debtors.add_command(label="View Account", command=self.view_debtor_account)
        self.debtors.add_separator()
        self.debtors.add_command(label="Account History", command=self.debtor_history)
        self.debtors.add_command(label="Track Accounts", command=self.accounts_receivable_tracking)

        # ************** Creditors ***************************
        self.creditors = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Accounts Payable", menu=self.creditors)
        self.creditors.add_command(label="Accounts", command=self.accounts_payable)
        # self.creditors.add_command(label="Update Account")
        # self.creditors.add_command(label="Creditors List")
        self.creditors.add_command(label="View Account", command=self.view_creditor_account)
        self.creditors.add_separator()
        self.creditors.add_command(label="Account History", command=self.creditor_account_history)
        self.creditors.add_command(label="Track Accounts", command=self.accounts_payable_tracking)

        # ************** Purchases ***************************
        self.purchases = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Purchases", menu=self.purchases)
        # self.purchases.add_command(label="Purchases Account")
        self.purchases.add_command(label="Invoice", command=self.purchase_invoice)
        # self.purchases.add_command(label="View Invoice")
        self.purchases.add_separator()
        self.purchases.add_command(label="Track Purchases", command=self.track_purchases)

        # ************** Sales ***************************
        self.sales = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Sales", menu=self.sales)
        # self.sales.add_command(label="Sales Account")
        self.sales.add_command(label="Invoice", command=self.sales_invoice)
        # self.sales.add_command(label="View Invoice")
        self.sales.add_separator()
        self.sales.add_command(label="Track Sales", command=self.track_sales)

        # ****************** Expenditure ********************
        self.expenses = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Expenditure", menu=self.expenses)
        self.expenses.add_command(label="Create/Modify", command=self.expenditure)
        self.expenses.add_separator()
        self.expenses.add_command(label="Track Expenses", command=self.track_expenditure)

        # ****************** Reports **********************
        self.report = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Reports", menu=self.report)
        self.report.add_command(label="Accounts Payable", command=self.accounts_payable_report_window)
        self.report.add_command(label="Accounts Receivable", command=self.accounts_receivable_report_window)
        self.report.add_separator()
        self.report.add_command(label="Purchases Account", command=self.purchase_report_window)
        self.report.add_command(label="Sales Account", command=self.sales_report_window)
        self.report.add_separator()
        self.report.add_command(label="Inventory", command=self.inventory_report_window)
        self.report.add_separator()
        self.report.add_command(label="Expenses Account", command=self.exp_account_report)
        self.report.add_separator()
        self.report.add_command(label="Profit or Loss", command=self.profit_or_loss_report_window)

        # *************** Help Menu ********************
        self.help_menu = Menu(self.drop_down_menus, tearoff=0)
        self.drop_down_menus.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.about_window)
        self.help_menu.add_command(label="Exit", command=self.exit_command)

        # self.btn = Button(self.master, text="button", command=self.inventory_input).grid(row=0, column=1)

    def exit_command(self):
        """ Exit Command """
        query = mbx.askyesno("Confirm Exit", "Do you want to exit Py Accounting Solutions?")
        if query is True:
            ##################################
            # CLOSES ALL THE DATABASE OPENED
            ##################################
            i_data.close_database()
            t_inv.close_database()
            d_data.close_database()
            t_debtors.close_database()
            debtor.close_database()
            debtor_history.close_database()
            c_data.close_database()
            t_creditors.close_database()
            creditor.close_database()
            creditor_history.close_database()
            s_data.close_database()
            t_sales.close_database()
            p_data.close_database()
            t_purchases.close_database()
            e_data.close_database()
            t_expenses.close_database()
            self.master.destroy()

    def about_window(self):
        """ About Window """
        window = Toplevel()
        window.title("About Window")
        window.resizable(height=False, width=False)

        about_label = Label(window, font=("Times New Roman", 16),
                            text="Py Accounting Solutions Version 1.0\nMade by: Afriyie Daniel"
                                 "\n\n\nemail: afriyiedaniel1@outlook.com\nTel: 0543833501/0502155025\n"
                                 "The Drive to Develop\n\n").grid(row=1, column=1)

        about_label_2 = Label(window, text="Copyright 2018-2019 Py Accounting Solutions",
                              font=("Monotype Corsiva", 12)).grid(row=2, column=1)

        about_btn = Button(window, text="Ok", width=15, relief=RIDGE, command=window.destroy) \
            .grid(row=3, column=1)

        window.mainloop()

    ##########################################
    #               MENU COMMANDS
    ##########################################
    def inventory_input(self):
        """ Data Entry Window """
        inventory_window.InventoryInput(self)

    def inventory_tracking(self):
        """ Inventory Tracking Window """
        inventory_window.TrackInventory(self)

    def inventory_report_window(self):
        """ Inventory Report Window """
        inventory_report.InventoryReport(self)

    def accounts_receivable(self):
        """ Debtors Window """
        debtors_window.Accounts(self)

    def accounts_receivable_tracking(self):
        """ Accounts Receivable Tracking Window """
        debtors_window.TrackAccountsReceivable(self)

    def accounts_receivable_report_window(self):
        """ Accounts Receivable Reports Window """
        accounts_receivable_report.AccountsReceivableReport(self)

    def view_debtor_account(self):
        """ View Debtor's Account Window """
        debtors_window.ViewAccount(self)

    def debtor_history(self):
        """ Debtor Account History Window """
        debtors_window.AccountHistory(self)

    def accounts_payable(self):
        """ Accounts Payable Window"""
        creditors_window.Accounts(self)

    def accounts_payable_tracking(self):
        """ Accounts Payable Tracking Window"""
        creditors_window.TrackAccountsPayable(self)

    def view_creditor_account(self):
        """ View Creditor's Account Window """
        creditors_window.ViewAccount(self)

    def creditor_account_history(self):
        """ Creditor Account History Window"""
        creditors_window.AccountHistory(self)

    def accounts_payable_report_window(self):
        """ View Accounts Payable Report Window"""
        accounts_payable_report.AccountsPayableReport(self)

    def sales_invoice(self):
        """ Sales Invoice Window """
        sales_window.CreateInvoice(self)

    def track_sales(self):
        """ Sales Tracking Window """
        sales_window.TrackSales(self)

    def sales_report_window(self):
        """ Sales Report Window """
        sales_report.SalesReport(self)

    def purchase_invoice(self):
        """ Purchase Invoice Window """
        purchase_window.CreateInvoice(self)

    def track_purchases(self):
        """ Purchase Tracking Window """
        purchase_window.TrackPurchases(self)

    def purchase_report_window(self):
        """ Purchase Report Window """
        purchase_report.PurchaseReport(self)

    def expenditure(self):
        """ Expenditure Window """
        expenditure_window.Expenses(self)

    def track_expenditure(self):
        """ Track Expenditure Window """
        expenditure_window.TrackExpenditure(self)

    def exp_account_report(self):
        """ Expense Account Report Window """
        expense_report.ExpenseReport(self)

    def profit_or_loss_report_window(self):
        """ Profit or Loss Report Window """
        profit_or_loss_report.ProfitOrLoss(self)
