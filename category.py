from  tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk,messagebox
import sqlite3 as sq
from speak import Speak_thread
import json
class Category:
    def __init__(self, master):
        self.root=master
        f = open('settings.json',)
        data = json.load(f)
        self.bg_color=data['bg']
        self.fg_color=data['fg']


        self.cat_id=StringVar()
        self.cat_name=StringVar()

        self.img1= Image.open("images\\img1.jpg")
        self.img1=self.img1.resize((400,245),Image.ANTIALIAS)
        self.img1 =  ImageTk.PhotoImage(self.img1)

        self.img2= Image.open("images\\img2.jpg")
        self.img2=self.img2.resize((420,245),Image.ANTIALIAS)
        self.img2 =  ImageTk.PhotoImage(self.img2)

        intro_lbl=Label(self.root,text="Manage Product Category",bg="gray",fg="white",font=("time new roman",30,"bold"),bd=2,relief=RIDGE).pack(fill=X,side=TOP,padx=80,pady=20)
        
        self.img1_lbl=Label(self.root,image=self.img1)
        self.img1_lbl.place(x=100,y=300)
        self.img2_lbl=Label(self.root,image=self.img2)
        self.img2_lbl.place(x=505,y=300)

        name_lbl=Label(self.root,text="Enter Category Name",bg=self.bg_color,fg="white",font=("time new roman",23,"bold")).place(x=100,y=100)
        name_entry=Entry(self.root,textvariable=self.cat_name,font=("time new roman",15,"bold"),bg='white').place(x=100,y=160,width=280,height=35)
        
        add_btn=Button(self.root,text="Add",command=self.insert,bg="black",fg="white",font=("time new roman",16,"bold"),cursor='hand2').place(x=100,y=220,width=140,height=35)
        delete_btn=Button(self.root,text="Delete",command=self.delete,bg="black",fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=240,y=220,width=140,height=35)

        Detail_frame=Frame(self.root,bd=3,relief=RIDGE,bg="black")
        Detail_frame.place(x=460,y=100,width=470,height=180)

        scrolly=Scrollbar(Detail_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)
        scrollx=Scrollbar(Detail_frame,orient= HORIZONTAL)
        scrollx.pack(fill=X,side=BOTTOM)

        fields=("Id","Category Name")
        self.cat_table=ttk.Treeview(Detail_frame,columns=fields,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.cat_table.pack(fill=BOTH,expand=1)
        for field in fields:
            self.cat_table.heading(field,text=field)
        for field in fields:
            self.cat_table.column(field,width=100)
        self.cat_table["show"]="headings"
        scrollx.config(command=self.cat_table.xview)
        scrolly.config(command=self.cat_table.yview)
        self.show_table()
        self.cat_table.bind("<Double-Button-1>",self.get_data)

    def insert(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.cat_name.get()=="":
                Speak_thread("Category Name must be required")
                messagebox.showerror("Error","Category Name must be required")
            else:
                cur.execute("select * from Category where Name=?",(self.cat_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category Name already exist")
                else:
                    cur.execute("insert into Category (Name) values(?)",(self.cat_name.get(),))
                    conn.commit()
                    Speak_thread("Category inserted sucessfully")
                    messagebox.showinfo("sucessfull","Category inserted sucessfully")
                    self.show_table()
        except Exeption as error:
            messagebox.showerror("Error",error)
    def delete(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.cat_name.get()=="":
                Speak_thread("Please Enter Category Name ")
                messagebox.showerror("Error","Please select or Enter Category Name")
            else:
                cur.execute("select * from Category where Name=?",(self.cat_name.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category Name")
                else:
                    Speak_thread("Are you sure sir")
                    option=messagebox.askyesno("Confirm","Do you want to delete")
                    if option==True:
                        cur.execute("delete from Category where Name=?",(self.cat_name.get(),))
                        conn.commit()
                        Speak_thread("Category deleted sucessfully")
                        messagebox.showinfo("sucessfull"," Category deleted sucessfully")
                        self.show_table()
                        self.cat_name.set("")
        except Exeption as error:
            messagebox.showerror("Error",error)
    def show_table(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            cur.execute("select * from Category")
            rows=cur.fetchall()
            self.cat_table.delete(*self.cat_table.get_children())
            for row in rows:
                self.cat_table.insert('',END,values=row)
        except Exeption as error:
            messagebox.showerror("Error",error)
    def search(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.sup_searchtxt.get()=="":
                messagebox.showerror("Error","Enter Invoice id")
            else:
                cur.execute("select * from Supplier where Sup_id=?",(self.sup_searchtxt.get(),))
                rows=cur.fetchone()
                if rows!=None:
                    self.cat_table.delete(*self.cat_table.get_children())
                    self.cat_table.insert('',END,values=rows)
                else:
                    messagebox.showinfo("Record","No record found")
        except Exeption as error:
            messagebox.showerror("Error",error)
    def get_data(self,event):
        f=self.cat_table.focus()
        content=(self.cat_table.item(f))
        row=content["values"]
        self.cat_name.set(row[1])

        

if __name__ == '__main__':
    root=Tk()
    Inv=Category(root)
    root.mainloop()