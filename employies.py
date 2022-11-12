from  tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk,messagebox
import sqlite3 as sq
from speak import Speak_thread
import json

class Employee:
    def __init__(self, master):
        self.root=master  
        f = open('settings.json',)
        data = json.load(f)
        self.bg_color=data['bg']
        self.fg_color=data['fg']

        self.emp_searchby=StringVar()
        self.emp_searchtxt=StringVar()
        self.emp_id=StringVar()
        self.emp_gender=StringVar()
        self.emp_contact=StringVar()
        self.emp_name=StringVar()
        self.emp_dob=StringVar()
        self.emp_doj=StringVar()
        self.emp_email=StringVar()
        self.emp_password=StringVar()
        self.emp_type=StringVar()
        self.emp_salary=StringVar()

        search_frame=LabelFrame(self.root,text="Search Employee",bg=self.bg_color,fg="white",bd=2,relief=RIDGE,font=("time new roman",12,"bold"))
        options=ttk.Combobox(search_frame,textvariable=self.emp_searchby,values=("Select","Name","Email","Contact"),state='readonly',justify=CENTER,font=("time new roman",16,"bold"))
        options.place(x=10,y=10,width=180,height=30)
        options.current(0)
        Name_entry=Entry(search_frame,textvariable=self.emp_searchtxt,font=("time new roman",15,"bold"),bg='white')
        Name_entry.place(x=200,y=10)
        Name_entry.bind("<Return>",self.search)
        search_btn=Button(search_frame,command=self.search,text="Search",font=("time new roman",13,"bold"),bg='black',fg='white',cursor='hand2').place(x=450,y=8,width=120)
        search_frame.place(x=200,y=15,width=600,height=75)
        


        intro_lbl=Label(self.root,text="Employee Details",bg="gray",fg="white",font=("time new roman",17,"bold")).place(x=50,y=110,width=1000)
        
        id_lbl=Label(self.root,text="Emp id",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=100,y=160)
        gender_lbl=Label(self.root,text="Gender",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=420,y=160)
        contact_lbl=Label(self.root,text="Contact",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=750,y=160)
        name_lbl=Label(self.root,text="Name",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=100,y=200)
        dob_lbl=Label(self.root,text="D.O.B",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=420,y=200)
        doj_lbl=Label(self.root,text="D.O.J",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=750,y=200)
        email_lbl=Label(self.root,text="Email",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=100,y=240)
        password_lbl=Label(self.root,text="Password",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=420,y=240)
        utype_lbl=Label(self.root,text="User Type",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=750,y=240)
        address_lbl=Label(self.root,text="Address",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=100,y=280)
        salary_lbl=Label(self.root,text="Salary",bg=self.bg_color,fg="white",font=("time new roman",14,"bold")).place(x=750,y=280)
        
        id_entry=Entry(self.root,state="readonly",textvariable=self.emp_id,font=("time new roman",15,"bold"),bg='white').place(x=200,y=160,width=180)
        gender_options=ttk.Combobox(self.root,textvariable=self.emp_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("time new roman",16,"bold"))
        gender_options.place(x=520,y=160,width=180)
        gender_options.current(0)
        contact_entry=Entry(self.root,textvariable=self.emp_contact,font=("time new roman",15,"bold"),bg='white').place(x=850,y=160,width=180)
        name_entry=Entry(self.root,textvariable=self.emp_name,font=("time new roman",15,"bold"),bg='white').place(x=200,y=200,width=180)
        dob_entry=Entry(self.root,textvariable=self.emp_dob,font=("time new roman",15,"bold"),bg='white').place(x=520,y=200,width=180)
        doj_entry=Entry(self.root,textvariable=self.emp_doj,font=("time new roman",15,"bold"),bg='white').place(x=850,y=200,width=180)
        email_entry=Entry(self.root,textvariable=self.emp_email,font=("time new roman",15,"bold"),bg='white').place(x=200,y=240,width=180)
        password_entry=Entry(self.root,show="*",textvariable=self.emp_password,font=("time new roman",15,"bold"),bg='white').place(x=520,y=240,width=180)
        user_options=ttk.Combobox(self.root,textvariable=self.emp_type,values=("Select","Admin","Employee"),state='readonly',justify=CENTER,font=("time new roman",16,"bold"))
        user_options.place(x=850,y=240,width=180)
        user_options.current(0)
        self.txt_address=Text(self.root,font=("time new roman",14,"bold"))
        self.txt_address.place(x=200,y=280,width=320,height=60)
        salary_entry=Entry(self.root,textvariable=self.emp_salary,font=("time new roman",15,"bold"),bg='white').place(x=850,y=280,width=180)

        save_btn=Button(self.root,text="Save",command=self.insert,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=530,y=315,width=110,height=28)
        update_btn=Button(self.root,text="Update",command=self.update,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=660,y=315,width=110,height=28)
        delete_btn=Button(self.root,text="Delete",command=self.delete,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=790,y=315,width=110,height=28)
        clear_btn=Button(self.root,text="clear",command=self.clear,bg='black',fg="white",font=("time new roman",14,"bold"),cursor='hand2').place(x=920,y=315,width=110,height=28)

        Detail_frame=Frame(self.root,bd=3,relief=RIDGE,bg=self.bg_color)
        scrolly=Scrollbar(Detail_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)
        scrollx=Scrollbar(Detail_frame,orient= HORIZONTAL)
        scrollx.pack(fill=X,side=BOTTOM)

        fields=("Emp id","Name","Email","Gender","Contact","DOB","DOJ","Password","Emp Type","Address","Salary")
        self.emp_table=ttk.Treeview(Detail_frame,columns=fields,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.emp_table.pack(fill=BOTH,expand=1)
        for field in fields:
            self.emp_table.heading(field,text=field)
        for field in fields:
            self.emp_table.column(field,width=100)
        self.emp_table["show"]="headings"
        scrollx.config(command=self.emp_table.xview)
        scrolly.config(command=self.emp_table.yview)
        Detail_frame.place(x=40,y=350,width=1000,height=200)
        self.show_table()
        self.emp_table.bind("<Double-Button-1>",self.get_data)
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
        cur.execute("select * from Employee")
        emp_id="Emp"+str(len(cur.fetchall())+1)
        self.emp_id.set(emp_id)



    def insert(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            emp_id=self.emp_id.get().replace('Emp',"")
            if self.emp_name.get()=="" or self.emp_email.get()=="" or self.txt_address.get("1.0",END)=="" or self.emp_gender.get()=="Select" or self.emp_dob.get()=="" or self.emp_doj.get()=="" or self.emp_password.get()=="" or self.emp_type.get()=="Select" or self.emp_salary.get()=="":
                Speak_thread("All fields must be required")
                messagebox.showerror("Error","All fields must be required")
            else:
                cur.execute("select * from Employee where Emp_id=?",(emp_id,))
                row=cur.fetchone()
                if row!=None:
                    Speak_thread(" Employee Id already exist")
                    messagebox.showerror("Error"," Employee Id already exist")
                else:
                    cur.execute("insert into Employee (Emp_id,Name,Email,Gender,Contact,DOB,DOJ,Password,Emp_Type,Address,Salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                    emp_id,self.emp_name.get(),self.emp_email.get(),self.emp_gender.get(),self.emp_contact.get(),self.emp_dob.get(),
                        self.emp_doj.get(),self.emp_password.get(),self.emp_type.get(),self.txt_address.get("1.0",END),self.emp_salary.get()
                        
                    ))

                    conn.commit()
                    Speak_thread(f"{self.emp_name.get()} is added as {self.emp_type.get()} and his id is {str(self.emp_id.get())}")
                    messagebox.showinfo("sucessfull","Data inserted sucessfully ")
                    self.show_table()
                    self.clear()
        except Exeption as error:
            Speak_thread(" Error in added Employee")
            messagebox.showerror("Error",error)
    def update(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            emp_id=self.emp_id.get().replace("Emp","")
            cur.execute("select * from Employee where Emp_id=?",(emp_id,))
            row=cur.fetchone()
            if row==None:
                Speak_thread("Invalid Employee id")
                messagebox.showerror("Error","Invalid Employee id")
            else:
                cur.execute("update Employee set Name=?,Email=?,Gender=?,Contact=?,DOB=?,DOJ=?,Password=?,Emp_Type=?,Address=?,Salary=? where Emp_id=?",(
                    self.emp_name.get(),self.emp_email.get(),self.emp_gender.get(),self.emp_contact.get(),self.emp_dob.get(),
                    self.emp_doj.get(),self.emp_password.get(),self.emp_type.get(),self.txt_address.get("1.0",END),self.emp_salary.get(),
                    emp_id,
                    
                ))

                conn.commit()
                Speak_thread(f"id {str(self.emp_id.get())} is Updated sucessfully")
                messagebox.showinfo("sucessfull"," Data Updated sucessfully ")
                self.show_table()
        except Exeption as error:
            messagebox.showerror("Error",error)
    def show_table(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            cur.execute("select * from Employee")
            rows=cur.fetchall()
            self.emp_table.delete(*self.emp_table.get_children())
            for row in rows:
                self.emp_table.insert('',END,values=row)
        except Exeption as error:
            messagebox.showerror("Error",error)

    def delete(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            emp_id=self.emp_id.get().replace("Emp","")
            cur.execute("select * from Employee where Emp_id=?",(emp_id,))
            row=cur.fetchone()
            if row==None:
                Speak_thread("Invalid Employee id")
                messagebox.showerror("Error","Invalid Employee id")
            else:
                Speak_thread("Are you sure sir")
                option=messagebox.askyesno("Confirm","Do you want to delete")
                if option==True:
                    cur.execute("delete from Employee where Emp_id=?",(emp_id,))
                    conn.commit()
                    Speak_thread(f"{str(self.emp_id.get())} is deleted sucessfully")
                    messagebox.showinfo("sucessfull"," Data deleted sucessfully ")
                    self.clear()
        except Exeption as error:
            Speak_thread("error in deleting data")
            messagebox.showerror("Error",error)
    def show_table(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            cur.execute("select * from Employee")
            rows=cur.fetchall()
            self.emp_table.delete(*self.emp_table.get_children())
            for row in rows:
                self.emp_table.insert('',END,values=row)
        except Exeption as error:
            messagebox.showerror("Error",error)
    def search(self,event=None):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
    
        try:
            if self.emp_searchby.get()=="Select":
                Speak_thread("Select option for search")
                messagebox.showerror("Error","Select option for search")
            elif self.emp_searchtxt.get()=="":
                Speak_thread("Enter Text which you want to search")
                messagebox.showerror("Error","Enter Text which you want\n to search")
            else:
                cur.execute("select * from Employee where "+self.emp_searchby.get()+" LIKE '%"+self.emp_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    Speak_thread(f"{str(len(rows))} records found in database")
                    self.emp_table.delete(*self.emp_table.get_children())
                    for row in rows:
                        self.emp_table.insert('',END,values=row)
                else:
                    Speak_thread("No record found in database")
                    messagebox.showerror("Error","No record found in database")
        except Exeption as error:
            messagebox.showerror("Error",error)

        
        
    def get_data(self,event):
        f=self.emp_table.focus()
        content=(self.emp_table.item(f))
        row=content["values"]
        self.emp_id.set("Emp"+str(row[0]))
        self.emp_name.set(row[1])
        self.emp_email.set(row[2])
        self.emp_gender.set(row[3])
        self.emp_contact.set(row[4])
        self.emp_dob.set(row[5])
        self.emp_doj.set(row[6])
        self.emp_password.set(row[7])
        self.emp_type.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.emp_salary.set(row[10])

    def clear(self):
        conn=sq.connect(database=r'IMS.db')
        cur=conn.cursor()
        cur.execute("select * from Employee")
        emp_id="Emp"+str(len(cur.fetchall())+1)
        self.emp_id.set(emp_id)
        self.emp_name.set("")
        self.emp_email.set("")
        self.emp_gender.set("Select")
        self.emp_contact.set("")
        self.emp_dob.set("")
        self.emp_doj.set("")
        self.emp_password.set("")
        self.emp_type.set("Select")
        self.txt_address.delete('1.0',END)
        self.emp_salary.set("")
        self.emp_searchby.set("Select")
        self.emp_searchtxt.set("")
        self.show_table()

        

if __name__ == '__main__':
    root=Tk()
    Inv=Employee(root)
    root.mainloop()