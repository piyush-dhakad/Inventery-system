from  tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk,messagebox
import sqlite3 as sq
from speak import Speak_thread
import json
class Supplier:
    def __init__(self, master):
        self.root=master
        f = open('settings.json',)
        data = json.load(f)
        self.bg_color=data['bg']
        self.fg_color=data['fg'] 

        self.sup_searchtxt=StringVar()

        self.sup_id=StringVar()
        self.sup_contact=StringVar()
        self.sup_name=StringVar()

        search_frame=LabelFrame(self.root,text="Search Supplier",bg=self.bg_color,fg="white",bd=2,relief=RIDGE,font=("time new roman",12,"bold"))
        search_frame.place(x=70,y=430,width=450,height=110)

        supply_lbl=Label(search_frame,text="Search by Invoice no.",font=("time new roman",12,"bold"),bg=self.bg_color,fg="white")
        supply_lbl.place(x=40,y=10)

        Name_entry=Entry(search_frame,textvariable=self.sup_searchtxt,font=("time new roman",15,"bold"),bg='white')
        Name_entry.place(x=40,y=40)
        Name_entry.bind("<Return>",self.search)
        search_btn=Button(search_frame,command=self.search,text="Search",font=("time new roman",13,"bold"),bg='black',fg='white',cursor='hand2').place(x=290,y=38,width=120)
        intro_lbl=Label(self.root,text="Supplier Details",bg="gray",fg="white",font=("time new roman",20,"bold")).place(x=50,y=30,width=1000,height=40)
        
        id_lbl=Label(self.root,text="Invoice id",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=70,y=100)
        name_lbl=Label(self.root,text="Name",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=70,y=140)
        contact_lbl=Label(self.root,text="Contact",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=70,y=180)
        desc_lbl=Label(self.root,text="Description",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=70 ,y=220)

        id_entry=Entry(self.root,state="readonly",textvariable=self.sup_id,font=("time new roman",15,"bold"),bg='white').place(x=200,y=100,width=180)
        name_entry=Entry(self.root,textvariable=self.sup_name,font=("time new roman",15,"bold"),bg='white').place(x=200,y=140,width=180)
        contact_entry=Entry(self.root,textvariable=self.sup_contact,font=("time new roman",15,"bold"),bg='white').place(x=200,y=180,width=180)
        self.txt_dsc=Text(self.root,font=("time new roman",14,"bold"))
        self.txt_dsc.place(x=200,y=220,width=320,height=100)
        self.txt_dsc.bind("<Return>",self.insert)
        
        save_btn=Button(self.root,text="Save",command=self.insert,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=80,y=380,width=110,height=35)
        update_btn=Button(self.root,text="Update",command=self.update,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=190,y=380,width=110,height=35)
        delete_btn=Button(self.root,text="Delete",command=self.delete,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=300,y=380,width=110,height=35)
        clear_btn=Button(self.root,text="clear",command=self.clear,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=410,y=380,width=110,height=35)

        Detail_frame=Frame(self.root,bd=3,relief=RIDGE,bg=self.bg_color)
        Detail_frame.place(x=550,y=100,width=500,height=440)

        scrolly=Scrollbar(Detail_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)
        scrollx=Scrollbar(Detail_frame,orient= HORIZONTAL)
        scrollx.pack(fill=X,side=BOTTOM)

        fields=("Invoice","Name","Contact","Description")
        self.sub_table=ttk.Treeview(Detail_frame,columns=fields,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.sub_table.pack(fill=BOTH,expand=1)
        for field in fields:
            self.sub_table.heading(field,text=field)
        for field in fields:
            self.sub_table.column(field,width=100)
        self.sub_table["show"]="headings"
        scrollx.config(command=self.sub_table.xview)
        scrolly.config(command=self.sub_table.yview)
        self.show_table()
        self.sub_table.bind("<Double-Button-1>",self.get_data)
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
        cur.execute("select * from Supplier")
        sup_id="Sup"+str(len(cur.fetchall())+1)
        self.sup_id.set(sup_id)

    def insert(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            sup_id=self.sup_id.get().replace('Sup',"")
            if self.sup_name.get()=="" or self.sup_contact.get()=="" or self.txt_dsc.get("1.0",END)=="":
                Speak_thread("All fields must be required ")
                messagebox.showerror("Error","All fields will be required")
            else:
                cur.execute("select * from Supplier where Sup_id=?",(sup_id,))
                row=cur.fetchone()
                if row!=None:
                    Speak_thread("Invoice id already exist")
                    messagebox.showerror("Error","Invoice Id already exist")
                else:
                    cur.execute("insert into Supplier (Sup_id,Name,Contact,Description) values(?,?,?,?)",(
                            sup_id,self.sup_name.get(),self.sup_contact.get(),self.txt_dsc.get("1.0",END)
                        
                    ))

                    conn.commit()
                    Speak_thread(f"{self.sup_name.get()} is added and id is {self.sup_id.get()}")
                    messagebox.showinfo("sucessfull","Data inserted sucessfully")
                    self.clear()
        except Exeption as error:
            messagebox.showerror("Error",error)
    def update(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            sup_id=self.sup_id.get().replace("Sup","")
            cur.execute("select * from Supplier where Sup_id=?",(sup_id,))
            row=cur.fetchone()
            if row==None:
                Speak_thread("Invalid Invoice id")
                messagebox.showerror("Error","Invalid Invoice id")
            else:
                cur.execute("update Supplier set Name=?,Contact=?,Description=? where Sup_id=?",(
                    self.sup_name.get(),self.sup_contact.get(),self.txt_dsc.get("1.0",END), sup_id,
                    
                ))
                conn.commit()
                Speak_thread("data updated sucessfully")
                messagebox.showinfo("sucessfull"," Data updated sucessfully")
                self.clear()
        except Exeption as error:
            Speak_thread("error in updating")
            messagebox.showerror("Error",error)
    def show_table(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            cur.execute("select * from Supplier")
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
            sup_id=self.sup_id.get().replace("Sup","")
            cur.execute("select * from Supplier where Sup_id=?",(sup_id,))
            row=cur.fetchone()
            if row==None:
                Speak_thread("Invalid Invoice id")
                messagebox.showerror("Error","Invalid Invoice id")
            else:
                Speak_thread("Are you sure sir")
                option=messagebox.askyesno("Confirm","Do you want to delete")
                if option==True:
                    cur.execute("delete from Supplier where Sup_id=?",(sup_id,))
                    conn.commit()
                    Speak_thread("row deleted sucessfully")
                    messagebox.showinfo("sucessfull"," Data deleted sucessfully")
                    self.clear()
        except Exeption as error:
            Speak_thread("Error in deleting data")
            messagebox.showerror("Error",error)
    def show_table(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            cur.execute("select * from Supplier")
            rows=cur.fetchall()
            self.sub_table.delete(*self.sub_table.get_children())
            for row in rows:
                self.sub_table.insert('',END,values=row)
        except Exeption as error:
            messagebox.showerror("Error",error)
    def search(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.sup_searchtxt.get()=="":
                Speak_thread("Please Enter Invoice id")
                messagebox.showerror("Error","Enter Invoice id")
            else:
                sup_id=self.sup_searchtxt.get().lower().replace("sup","")
                cur.execute("select * from Supplier where Sup_id=?",(sup_id,))
                rows=cur.fetchone()
                if rows!=None:
                    Speak_thread("records showing in table")
                    self.sub_table.delete(*self.sub_table.get_children())
                    self.sub_table.insert('',END,values=rows)
                else:
                    Speak_thread("No record found ")
                    messagebox.showinfo("Record","No record found")
        except Exeption as error:
            Speak_thread("error in searching")
            messagebox.showerror("Error",error)
    def get_data(self,event):
        f=self.sub_table.focus()
        content=(self.sub_table.item(f))
        row=content["values"]
        self.sup_id.set("Sup"+str(row[0]))
        self.sup_name.set(row[1])
        self.sup_contact.set(row[2])
        self.txt_dsc.delete('1.0',END)
        self.txt_dsc.insert(END,row[3])

    def clear(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
        cur.execute("select * from Supplier")
        sup_id="Sup"+str(len(cur.fetchall())+1)
        self.sup_id.set(sup_id)
        self.sup_name.set("")
        self.sup_contact.set("")
        self.txt_dsc.delete('1.0',END)
        self.sup_searchtxt.set("")
        self.show_table()

        

if __name__ == '__main__':
    root=Tk()
    Inv=Supplier(root)
    root.mainloop()