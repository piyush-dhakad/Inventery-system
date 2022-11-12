from  tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk,messagebox
import sqlite3 as sq
from speak import Speak_thread
import json
class Product:
    def __init__(self, master):
        self.root=master
        f = open('settings.json',)
        data = json.load(f)
        self.bg_color=data['bg']
        self.fg_color=data['fg']


        self.Category_var=StringVar()
        self.pid_var=StringVar()
        self.sup_var=StringVar()
        self.name_var=StringVar()
        self.price_var=StringVar()
        self.qty_var=StringVar()
        self.status_var=StringVar()
        self.searchby_var=StringVar()
        self.searchtxt_var=StringVar()

        self.cat_list=[]
        self.sup_list=[]
        self.fetch_all()

        Pro_frame=Frame(self.root,bd=2,relief=RIDGE,bg=self.bg_color)
        Pro_frame.place(x=20,y=50,width=430,height=480)

        intro_lbl=Label(Pro_frame,text="Product Detail",bg="white",fg=self.bg_color,font=("time new roman",25,"bold")).pack(fill=X,side=TOP)
        Cat_lbl=Label(Pro_frame,text="Category",bg=self.bg_color,fg="white",font=("time new roman",18,"bold")).place(x=18,y=60)
        sup_lbl=Label(Pro_frame,text="Supplier",bg=self.bg_color,fg="white",font=("time new roman",18,"bold")).place(x=18,y=110)
        name_lbl=Label(Pro_frame,text="Pro. Name",bg=self.bg_color,fg="white",font=("time new roman",18,"bold")).place(x=18,y=160)
        price_lbl=Label(Pro_frame,text="Price",bg=self.bg_color,fg="white",font=("time new roman",18,"bold")).place(x=18,y=210)
        qty_lbl=Label(Pro_frame,text="Quantity",bg=self.bg_color,fg="white",font=("time new roman",18,"bold")).place(x=18,y=260)
        status_lbl=Label(Pro_frame,text="Status",bg=self.bg_color,fg="white",font=("time new roman",18,"bold")).place(x=18,y=310)

        cat_options=ttk.Combobox(Pro_frame,textvariable=self.Category_var,values=self.cat_list,state='readonly',justify=CENTER,font=("time new roman",16,"bold"))
        cat_options.place(x=150,y=65,width=180,height=30)
        cat_options.current(0)
        sup_options=ttk.Combobox(Pro_frame,textvariable=self.sup_var,values=self.sup_list,state='readonly',justify=CENTER,font=("time new roman",16,"bold"))
        sup_options.place(x=150,y=115,width=180,height=30)
        sup_options.current(0)
        name_entry=Entry(Pro_frame,textvariable=self.name_var,font=("time new roman",15,"bold"),bg='white').place(x=150,y=165,width=180)
        price_entry=Entry(Pro_frame,textvariable=self.price_var,font=("time new roman",15,"bold"),bg='white').place(x=150,y=215,width=180)
        qty_entry=Entry(Pro_frame,textvariable=self.qty_var,font=("time new roman",15,"bold"),bg='white').place(x=150,y=265,width=180)
        status_options=ttk.Combobox(Pro_frame,textvariable=self.status_var,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("time new roman",16,"bold"))
        status_options.place(x=150,y=315,width=180,height=30)
        status_options.current(0)

        save_btn=Button(Pro_frame,text="Save",command=self.insert,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=18,y=380,width=100,height=35)
        update_btn=Button(Pro_frame,text="Update",command=self.update,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=120,y=380,width=100,height=35)
        delete_btn=Button(Pro_frame,text="Delete",command=self.delete,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=220,y=380,width=100,height=35)
        clear_btn=Button(Pro_frame,text="clear",command=self.clear,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=320,y=380,width=100,height=35)
    
        search_frame=LabelFrame(self.root,text="Search Product",bg=self.bg_color,fg="white",bd=2,relief=RIDGE,font=("time new roman",12,"bold"))
        search_frame.place(x=470,y=50,width=600,height=75)

        options=ttk.Combobox(search_frame,textvariable=self.searchby_var,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("time new roman",16,"bold"))
        options.place(x=10,y=10,width=180,height=30)
        options.current(0)

        Name_entry=Entry(search_frame,textvariable=self.searchtxt_var,font=("time new roman",15,"bold"),bg='white')
        Name_entry.place(x=200,y=10)
        Name_entry.bind("<Return>",self.search)
        search_btn=Button(search_frame,command=self.search,text="Search",font=("time new roman",13,"bold"),bg='black',fg='white',cursor='hand2').place(x=450,y=8,width=120)
        

        Detail_frame=Frame(self.root,bd=3,relief=RIDGE,bg=self.bg_color)
        Detail_frame.place(x=470,y=130,width=600,height=400)

        scrolly=Scrollbar(Detail_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)
        scrollx=Scrollbar(Detail_frame,orient= HORIZONTAL)
        scrollx.pack(fill=X,side=BOTTOM)

        fields=("Pid","Category","Supplier","Name","Price","Quantity","status")
        self.sub_table=ttk.Treeview(Detail_frame,columns=fields,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.sub_table.pack(fill=BOTH,expand=1)
        for field in fields:
            self.sub_table.heading(field,text=field)
        for field in fields:
            self.sub_table.column(field,width=100)
        self.sub_table["show"]="headings"
        scrollx.config(command=self.sub_table.xview)
        scrolly.config(command=self.sub_table.yview)
        self.sub_table.bind("<Double-Button-1>",self.get_data)
        self.show_table()

    def fetch_all(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
           cur.execute("select Name from Category") 
           Cat=cur.fetchall()
           self.cat_list.append ("Empty")
           if len(Cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in Cat:
                    self.cat_list.append(i[0])
           cur.execute("select Name from Supplier") 
           sup=cur.fetchall()
           self.sup_list.append ("Empty")
           if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exeption as error:
            messagebox.showerror("Error",error)
    def insert(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.sup_var.get()=="Select" or self.name_var.get()=="" or self.Category_var.get=="Select":
                Speak_thread("All fields must be required")
                messagebox.showerror("Error","All fields will be required")
            else:
                cur.execute("select * from Product where Name=?",(self.name_var.get(),))
                row=cur.fetchone()
                if row!=None:
                    Speak_thread("This Product is already exist")
                    messagebox.showerror("Error"," This Product is already exist")
                else:
                    cur.execute("insert into Product (Category,Supplier,Name,Price,Quantity,Status) values(?,?,?,?,?,?)",(
                    self.Category_var.get(),self.sup_var.get(),self.name_var.get(),self.price_var.get(),
                    self.qty_var.get(),self.status_var.get()
                    ))

                    conn.commit()
                    Speak_thread("Product Added sucessfully")
                    messagebox.showinfo("sucessfull","Product Added sucessfully ")
                    self.show_table()
        except Exeption as error:
            messagebox.showerror("Error",error)
    def update(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.name_var.get()=="":
                Speak_thread("Product Name must be required")
                messagebox.showerror("Error","Product Name must be required")
            else:
                cur.execute("select * from Product where Name=?",(self.name_var.get(),))
                row=cur.fetchone()
                if row==None:
                    Speak_thread("Product is not in the list")
                    messagebox.showerror("Error","This Product not in the list")
                else:
                    cur.execute("update Product set Category=?,Supplier=?,Name=?,Price=?,Quantity=?,Status=? where Name=?",(
                        self.Category_var.get(),self.sup_var.get(),self.name_var.get(),self.price_var.get(),self.qty_var.get(),
                        self.status_var.get(),self.name_var.get()
                        
                    ))

                    conn.commit()
                    Speak_thread("Product Updated sucessfully")
                    messagebox.showinfo("sucessfull"," Product Updated sucessfully ")
                    self.show_table()
        except Exeption as error:
            messagebox.showerror("Error",error)

    def show_table(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            cur.execute("select * from Product")
            rows=cur.fetchall()
            self.sub_table.delete(*self.sub_table.get_children())
            for row in rows:
                self.sub_table.insert('',END,values=row)
        except Exeption as error:
            messagebox.showerror("Error",error)

    def delete(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.name_var.get()=="":
                Speak_thread("Product Name must be required")
                messagebox.showerror("Error","Product Name must be required")
            else:
                cur.execute("select * from Product where Name=?",(self.name_var.get(),))
                row=cur.fetchone()
                if row==None:
                    Speak_thread("Product not available in the list")
                    messagebox.showerror("Error","Product not available in the list")
                else:
                    Speak_thread("Are you sure sir")
                    option=messagebox.askyesno("Confirm","Do you want to delete")
                    if option==True:
                        cur.execute("delete from Product where Name=?",(self.name_var.get(),))
                        conn.commit()
                        Speak_thread("Product deleted sucessfully")
                        messagebox.showinfo("sucessfull"," Product deleted sucessfully ")
                        self.clear()
        except Exeption as error:
            messagebox.showerror("Error",error)
    def search(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.searchby_var.get()=="Select":
                Speak_thread("Select option for search")
                messagebox.showerror("Error","Select option for search")
            elif self.searchtxt_var.get()=="":
                Speak_thread("Enter Text which you want to search")
                messagebox.showerror("Error","Enter Text which you want\n to search")
            else:
                cur.execute(f"select * from Product where  {self.searchby_var.get()}='{self.searchtxt_var.get()}'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    Speak_thread("Product showing in table")
                    self.sub_table.delete(*self.sub_table.get_children())
                    for row in rows:
                        self.sub_table.insert('',END,values=row)
                else:
                    Speak_thread("no Product found in database")
                    messagebox.showerror("Error","No record found in database")
        except Exeption as error:
            messagebox.showerror("Error",error)
    def get_data(self,event):
        f=self.sub_table.focus()
        content=(self.sub_table.item(f))
        row=content["values"]
        self.pid_var.set(row[0])
        self.Category_var.set(row[1])
        self.sup_var.set(row[2])
        self.name_var.set(row[3])
        self.price_var.set(row[4])
        self.qty_var.set(row[5])
        self.status_var.set(row[6])

    def clear(self):
        self.Category_var.set("Select")
        self.sup_var.set("Select")
        self.name_var.set("")
        self.price_var.set("")
        self.qty_var.set("")
        self.status_var.set("Active")
        self.searchby_var.set("Select")
        self.searchtxt_var.set("")
        self.show_table()

        
        

if __name__ == '__main__':
    root=Tk()
    Inv=Product(root)
    root.mainloop()