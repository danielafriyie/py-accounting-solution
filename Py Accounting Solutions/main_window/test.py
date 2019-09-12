from tkinter import *
from tkinter import ttk
from datetime import datetime as dt
from inventory import inventory_data
from debtors import debtors_data


root = Tk()

d = ttk.Treeview(root)
d.pack()



root.mainloop()
