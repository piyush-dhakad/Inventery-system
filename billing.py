from  tkinter import *
from PIL import ImageTk, Image
from speak import Speak_thread
from tkinter import ttk,messagebox
import sqlite3 as sq
import time
import os
import tempfile
import json
class Billing:
    def __init__(self, master):
        f = open('settings.json',)
        data = json.load(f)
        self.bg_color=data['bg']
        self.fg_color=data['fg']
        self.root=master
        self.root.config(bg=self.bg_color)
        self.root.geometry('1350x700+0+0')
        self.root.title("Inventery Management System")
        self.root.iconbitmap('images\\logo.ico')
        self.root.state('zoomed')
        self.root.resizable(False, False)
        self.search_var=StringVar()
        self.name_var=StringVar()
        self.contact_var=StringVar()
        self.pid_var=StringVar()
        self.p_name=StringVar()
        self.p_price=StringVar()
        self.p_qty=StringVar()
        self.p_stock=StringVar()
        self.cal_txt=StringVar()
        self.cart_list=[]

        intro_lbl=Label(self.root,text="Inventery management system",bg=self.bg_color,fg="white",font=("arial",30,"bold")).pack(fill=X,pady=20)
        logout_btn=Button(self.root,text="Logout",command=self.logout,font=("arial",15,"bold"),cursor='hand1',bg="yellow",width=12,bd=0).place(x=1170,y=25)
        self.clock_lbl=Label(self.root,text="Inventery management system\t\tDate:- dd\\mm\\yyyy\t\tTime:- HH:MM",bg="gray",fg=self.bg_color,font=("arial",15,"bold"))
        self.clock_lbl.pack(fill=X)


        Pro_frame=Frame(self.root,bd=3,relief=RIDGE,bg=self.bg_color)
        Pro_frame.place(x=10,y=130,width=410,height=560)
        title_lbl=Label(Pro_frame,text="All Products",fg="white",bg="gray",font=("arial",25,"bold")).pack(fill=X)

        Pro_frame2=Frame(Pro_frame,bd=1,relief=RIDGE,bg=self.bg_color)
        Pro_frame2.place(x=2,y=50,width=400,height=90)
        searchinfo_lbl=Label(Pro_frame2,text="Product Name",bg=self.bg_color,fg="white",font=("arial",16)).place(x=5,y=45)
        search_txt=Entry(Pro_frame2,textvariable=self.search_var,font=("arial",15)).place(x=150,y=47,width=150)
        search_lbl=Label(Pro_frame2,text="Search Product | By Name",bg=self.bg_color,fg="gray",font=("arial",17,"bold")).place(x=5,y=5)
        search_btn=Button(Pro_frame2,text="Search",command=self.search,bg=self.bg_color,fg="white",cursor="hand2",font=("arial",14)).place(x=310,y=47,height=30,width=85)
        show_all=Button(Pro_frame2,text="Show All",command=self.show_table,bg=self.bg_color,fg="white",cursor="hand2",font=("arial",14)).place(x=310,y=10,height=30,width=85)

        Product_frame=Frame(Pro_frame,bd=3,relief=RIDGE,bg=self.bg_color)
        Product_frame.place(x=2,y=140,width=400,height=390)

        scrolly=Scrollbar(Product_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)
        scrollx=Scrollbar(Product_frame,orient= HORIZONTAL)
        scrollx.pack(fill=X,side=BOTTOM)

        fields=("P id","Name","Price","Stock","status")
        self.Product_table=ttk.Treeview(Product_frame,columns=fields,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.Product_table.pack(fill=BOTH,expand=1)
        for field in fields:
            self.Product_table.heading(field,text=field)
        for field in fields:
            self.Product_table.column(field,width=70)
        self.Product_table["show"]="headings"
        scrollx.config(command=self.Product_table.xview)
        scrolly.config(command=self.Product_table.yview)
        self.Product_table.bind("<Double-Button-1>",self.get_data)
        info_lbl=Label(Pro_frame,text="Note : ' Enter 0 QTY to remove the Product From cart '",anchor=W,fg="red",bg=self.bg_color,font=("arial",12,"italic")).pack(fill=X,side=BOTTOM)
        


        custom_frame=Frame(self.root,bd=3,relief=RIDGE,bg=self.bg_color)
        custom_frame.place(x=430,y=130,width=540,height=120)
        title_lbl=Label(custom_frame,text="Customer Detail",bg="white",font=("times new roman",18)).pack(fill=X)
        name_lbl=Label(custom_frame,text="Name",bg=self.bg_color,fg="white",font=("arial",18)).place(x=5,y=40)
        name_txt=Entry(custom_frame,textvariable=self.name_var,font=("arial",14)).place(x=90,y=45,width=150)
        contact_lbl=Label(custom_frame,text="Contact",bg=self.bg_color,fg="white",font=("arial",15)).place(x=250,y=40)
        contact_txt=Entry(custom_frame,textvariable=self.contact_var,font=("arial",14)).place(x=340,y=45,width=160)
        btn_=Label(custom_frame,text="Note : ' Both fields must be required '",bg=self.bg_color,fg="red",font=("times new roman",16),anchor=W).pack(fill=X,side=BOTTOM,padx=10)

        

        cart_frame=Frame(self.root,bd=1,relief=RIDGE,bg=self.bg_color)
        cart_frame.place(x=430,y=255,width=540,height=330)

        cal_frame=Frame(cart_frame,bd=5,relief=RIDGE,bg=self.bg_color)
        cal_frame.place(x=5,y=5,width=270,height=320)

        cal_input=Entry(cal_frame,bd=4,justify=RIGHT,relief=GROOVE,textvariable=self.cal_txt,font=("times new roman",18,"bold")).pack(fill=X,ipady=6)
        btn7=Button(cal_frame,text="7",command=lambda:self.cal_data(7),bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=0,y=50)
        btn4=Button(cal_frame,text="4",command=lambda:self.cal_data(4),bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=0,y=115)
        btn1=Button(cal_frame,text="1",command=lambda:self.cal_data(1),bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=0,y=180)
        btn0=Button(cal_frame,text="0",command=lambda:self.cal_data(0),bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=0,y=245)
        
        btn8=Button(cal_frame,command=lambda:self.cal_data(8),text="8",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=65,y=50)
        btn5=Button(cal_frame,command=lambda:self.cal_data(5),text="5",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=65,y=115)
        btn2=Button(cal_frame,command=lambda:self.cal_data(2),text="2",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=65,y=180)
        btnc=Button(cal_frame,command=lambda:self.cal_txt.set(""),text="C",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=65,y=245)
        
        btn9=Button(cal_frame,command=lambda:self.cal_data(7),text="9",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=130,y=50)
        btn6=Button(cal_frame,command=lambda:self.cal_data(6),text="6",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=130,y=115)
        btn3=Button(cal_frame,command=lambda:self.cal_data(3),text="3",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=130,y=180)
        btn_eq=Button(cal_frame,command=lambda:self.cal_txt.set(eval(self.cal_txt.get())),text="=",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=130,y=245)

        btn_add=Button(cal_frame,command=lambda:self.cal_data('+'),text="+",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=195,y=50)
        btn_min=Button(cal_frame,command=lambda:self.cal_data('-'),text="-",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=195,y=115)
        btn_mul=Button(cal_frame,command=lambda:self.cal_data('*'),text="*",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=195,y=180)
        btn_div=Button(cal_frame,command=lambda:self.cal_data('/'),text="/",bg=self.bg_color,fg="white",font=("arial",15,"bold"),bd=5,width=4,pady=10).place(x=195,y=245)

        sub_frame=Frame(cart_frame,bd=2,relief=RIDGE,bg=self.bg_color)
        sub_frame.place(x=278,y=5,width=255,height=320)
        self.ptitle_lbl=Label(sub_frame,text="Cart    Total Product: 0",fg="white",bg=self.bg_color,font=("arial",15,"bold"))
        self.ptitle_lbl.pack(fill=X)

        scrolly=Scrollbar(sub_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)
        scrollx=Scrollbar(sub_frame,orient= HORIZONTAL)
        scrollx.pack(fill=X,side=BOTTOM)

        fields=("P id","Name","Price","QTY")
        self.Cart_table=ttk.Treeview(sub_frame,columns=fields,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.Cart_table.pack(fill=BOTH,expand=1)
        for field in fields:
            self.Cart_table.heading(field,text=field)
        for field in fields:
            if field=="P id":
                self.Cart_table.column(field,width=30)
            else:
                self.Cart_table.column(field,width=60)
        self.Cart_table["show"]="headings"
        scrollx.config(command=self.Cart_table.xview)
        scrolly.config(command=self.Cart_table.yview)
        self.Cart_table.bind("<Double-Button-1>",self.get_cart_data)

        cart_options=Frame(self.root,bd=1,relief=RIDGE,bg=self.bg_color)
        cart_options.place(x=430,y=590,width=540,height=100)

        pname_lbl=Label(cart_options,text="Product Name",bg=self.bg_color,fg="white",font=("arial",16)).place(x=10,y=2)
        pname_entry=Entry(cart_options,textvariable=self.p_name,state="readonly",font=("arial",12)).place(x=13,y=33,width=140)
        price_lbl=Label(cart_options,text="Price Per QTY",bg=self.bg_color,fg="white",font=("arial",16)).place(x=200,y=2)
        price_txt=Entry(cart_options,textvariable=self.p_price,state="readonly",font=("arial",12)).place(x=200,y=33,width=140)
        qty_lbl=Label(cart_options,text="Quantity",bg=self.bg_color,fg="white",font=("arial",16)).place(x=400,y=2)
        qty_txt=Entry(cart_options,textvariable=self.p_qty,font=("arial",12)).place(x=380,y=33,width=140)
        self.stock_lbl=Label(cart_options,text="In Stock ",bg=self.bg_color,fg="white",font=("times new roman",15))
        self.stock_lbl.place(x=10,y=65)
        clear_btn=Button(cart_options,command=self.clear_cart,text="Clear",bg=self.bg_color,fg="white",cursor="hand2",font=("times new roman",14)).place(x=200,y=60,width=140)
        add_btn=Button(cart_options,command=self.add_cart,text="Add | Update cart",bg=self.bg_color,fg="white",cursor="hand2",font=("times new roman",14)).place(x=340,y=60,width=180)
        
        show_frame=Frame(self.root,bd=2,relief=RIDGE,bg=self.bg_color)
        show_frame.place(x=975,y=130,width=385,height=400)
        intro_lbl=Label(show_frame,text="Customer Bill Area",bg="gray",fg="white",font=("times new roman",20,"bold")).pack(fill=X)

        scrolly=Scrollbar(show_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)

        self.product_bill=Text(show_frame,yscrollcommand=scrolly.set,bg=self.bg_color,fg="white")
        self.product_bill.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.product_bill.yview)

        menu_frame=Frame(self.root,bd=2,relief=RIDGE,bg=self.bg_color)
        menu_frame.place(x=975,y=545,width=385,height=145)

        self.amnt_lbl=Label(menu_frame,text="Bill Amount\n0",bg="#8bc34a",bd=1,relief=RIDGE,fg="white",font=("times new roman",15,"bold"))
        self.amnt_lbl.place(x=5,y=15,width=140,height=70)
        self.disct_lbl=Label(menu_frame,text="Discount\n5%",bg="#8bc34a",bd=1,relief=RIDGE,fg="white",font=("times new roman",15,"bold"))
        self.disct_lbl.place(x=145,y=15,width=90,height=70)
        self.net_pay_lbl=Label(menu_frame,text="Net Pay\n0",bg="#8bc34a",bd=1,relief=RIDGE,fg="white",font=("times new roman",15,"bold"))
        self.net_pay_lbl.place(x=235,y=15,width=140,height=70)

        print_btn=Button(menu_frame,cursor="hand2",text="Print Bill",bg=self.bg_color,bd=1,relief=RIDGE,fg="white",font=("times new roman",15,"bold")).place(x=5,y=90,width=90,height=40)
        clear_all_btn=Button(menu_frame,command=self.clear_all,cursor="hand2",text="Clear All",bg=self.bg_color,bd=1,relief=RIDGE,fg="white",font=("times new roman",15,"bold")).place(x=96,y=90,width=120,height=40)
        genrate_btn=Button(menu_frame,command=self.genrate_bill,cursor="hand2",text="Generate/Save Bill",bg=self.bg_color,bd=1,relief=RIDGE,fg="white",font=("times new roman",14,"bold")).place(x=217,y=90,width=158,height=40)


        

        footer_lbl=Label(self.root,text="Welcome to Inventery management Project \n",bg="gray",fg="white",font=("arial",14,"bold")).pack(side=BOTTOM,fill=X)
        self.show_table()
        self.update_time()
    def logout(self):
        self.root.destroy()
        os.system('login.py')
    def genrate_bill(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        if self.name_var.get()=="" or self.contact_var.get()=="":
           messagebox.showerror("Error","Please Enter Name and Contact Number")
        elif len(self.cart_list)==0:
           messagebox.showerror("Error","Please add Product to cart")
        else:
            Product_id=int(time.strftime('%H%M%S'))+int(time.strftime('%d%m%y'))

            bill_top=f"""
\t\tInventary
    Phone No. 7693813997 , Tarana-456665
{str('='*45)}
  Customer Name : {self.name_var.get()}
  Customer No.  : {self.contact_var.get()}
  Bill no.      : {Product_id}\t\t\t   Date: {time.strftime('%d/%m/%y')}
{str('='*45)}
  Product Name\t\t\tQTY\tPrice
{str('='*45)}
  """

            bill_bottom=f"""
{str('='*45)}
  Bill Amount\t\t\tRs.{self.amount}
  Discount\t\t\tRs.{self.amount-self.net_pay}
  Bill Amount\t\t\tRs.{self.net_pay}
{str('='*45)}

        """
            self.product_bill.config(state='normal')
            self.product_bill.delete('1.0',END)
            self.product_bill.insert('1.0',bill_top)
            try:
                for row in self.cart_list:
                    p_id=row[0]
                    name=row[1]
                    qty=row[4]
                    if int(row[4])==0:
                        status="Inactive"
                    else:
                        status="Active"
                    self.product_bill.insert(END,f'\n  {name}\t\t\t{row[3]}\tRs.{str(float(row[2]))}')
                    cur.execute('Update Product set Quantity=? ,Status=? where Pid=?',(qty,status,p_id))
                    conn.commit()
                    self.show_table()
            except Exception as e:
                messagebox.showerror('Error',e)
            self.product_bill.insert(END,bill_bottom)
            file=open(f'bill/{str(Product_id)}.txt','w')
            file.write(self.product_bill.get('1.0',END))
            file.close()
            self.product_bill.config(state='disabled')

    def show_table(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            cur.execute("select Pid ,Name,Price,Quantity,Status from Product where Status='Active'")
            rows=cur.fetchall()
            self.Product_table.delete(*self.Product_table.get_children())
            for row in rows:
                self.Product_table.insert('',END,values=row)
        except Exeption as error:
            messagebox.showerror("Error",error)
    def search(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.search_var.get()=="":
                #Speak_thread("Enter Product Name you want to search")
                messagebox.showerror("Error","Enter Product Name you want\n to search")
            else:
                qu=f"select Pid ,Name,Price,Quantity,Status from Product where  Name LIKE '%{self.search_var.get()}%' and Status ='Active'"
                cur.execute(qu)
                rows=cur.fetchall()
                if len(rows)!=0:
                    #Speak_thread("Product showing in table")
                    self.Product_table.delete(*self.Product_table.get_children())
                    for row in rows:
                        self.Product_table.insert('',END,values=row)
                else:
                    #Speak_thread("no Product found in database")
                    messagebox.showerror("Error","No record found in database")
        except Exeption as error:
            messagebox.showerror("Error",error)
    def cal_data(self,num):
        num=self.cal_txt.get()+str(num)
        self.cal_txt.set(num)
    def bill_updates(self):
        self.amount=0
        for row in self.cart_list:
            self.amount=self.amount+float(row[2])
        self.net_pay=self.amount-(self.amount*5)/100
        self.amnt_lbl.config(text=f"Bill Amount\n{self.amount}")
        self.net_pay_lbl.config(text=f"Net Pay\n{self.net_pay}")
        self.ptitle_lbl.config(text=f"Cart    Total Product: {str(len(self.cart_list))}")
    def get_data(self,event):
        f=self.Product_table.focus()
        content=(self.Product_table.item(f))
        row=content["values"]
        self.pid_var.set(row[0])
        self.p_name.set(row[1])
        self.p_price.set(row[2])
        self.stock_lbl.config(text=f"In Stock {row[3]}")
        self.p_stock.set(row[3])
        self.p_qty.set(1)

    def get_cart_data(self,event):
        f=self.Cart_table.focus()
        content=(self.Cart_table.item(f))
        row=content["values"]

        self.pid_var.set(row[0])
        self.p_name.set(row[1])
        self.p_qty.set(row[3])
        price=float(row[2])/row[3]
        self.p_price.set(round(price))
        self.stock_lbl.config(text=f"In Stock {row[4]}")
    def add_cart(self):
        if self.pid_var.get()=="":
            messagebox.showerror("Error","Please select Product From list")
        elif self.p_qty.get()=="":
            messagebox.showerror("Error","Product Quantity must be required")
        if int(self.p_qty.get())>int(self.p_stock.get()):
            messagebox.showerror("Error","Product Quantity is greater than Stock")
        else:
            stock_rmn=int(self.p_stock.get())-int(self.p_qty.get())
            total_price=float(int(self.p_qty.get())*float(self.p_price.get()))
            data=[self.pid_var.get(),self.p_name.get(),total_price,self.p_qty.get(),stock_rmn]

            available='no'
            index_=0
            for item in self.cart_list:
                if self.pid_var.get()==item[0]:
                    available='yes'
                    break
                index_+=1
            if available=='yes':
                option=messagebox.askyesno('Confirm',"Product Already Exists\n Do you want To Update")
                if option == True:
                    if self.p_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][2]=total_price
                        self.cart_list[index_][3]=self.p_qty.get()
                        self.cart_list[index_][4]=stock_rmn
            else:
                self.cart_list.append(data)

            self.stock_lbl.config(text=f"In Stock {str(stock_rmn)}")
            self.show_cart()
            self.bill_updates()
    def show_cart(self):
        try:
            self.Cart_table.delete(*self.Cart_table.get_children())
            for row in self.cart_list:
                self.Cart_table.insert('',END,values=row)
        except Exeption as error:
            messagebox.showerror("Error",error)
    def clear_cart(self):
        self.pid_var.set('')
        self.p_name.set('')
        self.p_price.set('')
        self.p_qty.set('')
        self.p_stock.set('')
        self.stock_lbl.config(text="In Stock")

    def clear_all(self):
        self.name_var.set('')
        self.contact_var.set('')
        self.search_var.set('')
        del self.cart_list[:]
        self.product_bill.delete('1.0',END)
        self.clear_cart()
        self.show_table()
        self.show_cart()
        self.amnt_lbl.config(text="Bill Amount\n0")
        self.net_pay_lbl.config(text="Net Pay\n0")
        self.ptitle_lbl.config(text="Cart    Total Product: 0")
    def update_time(self):
        time_=str(time.strftime('%I:%M:%S'))
        date_=str(time.strftime('%d/%m/%y'))
        self.clock_lbl.config(text=f"Inventery management system\t\tDate:- {date_}\t\tTime:-{time_}")
        self.clock_lbl.after(200,self.update_time)
    def print_bill(self):
        if print_status==0:
            messagebox.showerror('Print','Please genrate bill first')
        else:
            pass
if __name__ == '__main__':
    root=Tk()
    Inv=Billing(root)
    root.mainloop()
