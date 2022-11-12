from  tkinter import *
from employies import Employee
from supplier import Supplier
from category import Category
from product import Product
from sales import Sale
import sqlite3 as sq
import os
from speak import Speak_thread
class Dashboard:
    def __init__(self, master):
        self.root=master
        valu=self.values()  

        self.employee_lbl=Button(self.root,command=lambda:self.Activate(1),text=f"Total Employees\n[{valu[0]}]",font=("new times roman",15,"bold"),bg="#33bbf9",bd=2,relief=RIDGE,height=6,width=20)
        self.employee_lbl.place(x=150,y=100)
        self.supplier_lbl=Button(self.root,command=lambda:self.Activate(2),text=f"Total Suppliers\n[{valu[1]}]",font=("new times roman",15,"bold"),bg="#ff5722",bd=2,relief=RIDGE,height=6,width=20)
        self.supplier_lbl.place(x=425,y=100)
        self.category_lbl=Button(self.root,command=lambda:self.Activate(3),text=f"Total Categories\n[{valu[2]}]",font=("new times roman",15,"bold"),bg="#009688",bd=2,relief=RIDGE,height=6,width=20)
        self.category_lbl.place(x=700,y=100)
        self.product_lbl=Button(self.root,command=lambda:self.Activate(4),text=f"Total Products\n[{valu[3]}]",font=("new times roman",15,"bold"),bg="#607d8b",bd=2,relief=RIDGE,height=6,width=20)
        self.product_lbl.place(x=275,y=280)
        self.Sale_lbl=Button(self.root,command=lambda:self.Activate(5),text=f"Total Sales\n[{valu[4]}]",font=("new times roman",15,"bold"),bg="#ffc107",bd=2,relief=RIDGE,height=6,width=20)
        self.Sale_lbl.place(x=550,y=280)
         
    def Activate(self,token):
        if token==1:
            Speak_thread("Entering Employee tab")
            self.Employee_win=Frame(self.root,bg="black")
            self.Employee_win.place(x=0,y=0,width=1090,height=568)
            self.Employee_obj=Employee(self.Employee_win)
        elif token==2:
            Speak_thread("Entering supplier tab")
            self.Supplier_win=Frame(self.root,bg="black")
            self.Supplier_win.place(x=0,y=0,width=1090,height=568)
            self.Supplier_obj=Supplier(self.Supplier_win)
        elif token==3:
            Speak_thread("Entering category tab")
            self.Category_win=Frame(self.root,bg="black")
            self.Category_win.place(x=0,y=0,width=1090,height=568)
            self.Category_win=Category(self.Category_win)
        elif token==4:
            Speak_thread("Entering product tab")
            self.Product_win=Frame(self.root,bg="black")
            self.Product_win.place(x=0,y=0,width=1090,height=568)
            self.Product_win=Product(self.Product_win)
        elif token==5:
            Speak_thread("Entering sales tab")
            self.Sale_win=Frame(self.root,bg="black")
            self.Sale_win.place(x=0,y=0,width=1090,height=568)
            self.Sale_win=Sale(self.Sale_win)
   
    def values(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
        cur.execute("select * from Employee")
        emp_total=cur.fetchall()
        cur.execute("select * from Supplier")
        sup_total=cur.fetchall()
        cur.execute("select * from Category")
        cat_total=cur.fetchall()
        cur.execute("select * from Product")
        pro_total=cur.fetchall()
        return [len(emp_total),len(sup_total),len(cat_total),len(pro_total),len(os.listdir('bill'))]

if __name__ == '__main__':
    root=Tk()
    Inv=Dashboard(root)
    root.mainloop()