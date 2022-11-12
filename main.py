from  tkinter import *
from PIL import ImageTk, Image
from employies import Employee
from supplier import Supplier
from category import Category
from product import Product
from dashboard import Dashboard
from sales import Sale
from speak import Speak_thread
import time
import os
import json
class Inventery:
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

        intro_lbl=Label(self.root,text="Inventery Management System",bg=self.bg_color,fg=self.fg_color,font=("arial",30,"bold")).pack(fill=X,pady=20)
        logout_btn=Button(self.root,text="Logout",command=lambda:self.Activate(12),font=("arial",15,"bold"),cursor='hand1',bg="yellow",width=12,bd=0).place(x=1170,y=25)
        self.clock_lbl=Label(self.root,bg="gray",fg=self.bg_color,font=("arial",15,"bold"))
        self.clock_lbl.pack(fill=X)

        button_frame=Frame(self.root,bd=2,bg=self.bg_color,width=400,height=565,relief=RIDGE)
        button_frame.place(x=0,y=124)
        self.intro_img= Image.open("images\\inventory.png")
        self.intro_img=self.intro_img.resize((260,250), Image.ANTIALIAS)
        self.intro_img =  ImageTk.PhotoImage(self.intro_img)
        intro_img_lbl=Label(button_frame,image=self.intro_img,bg=self.bg_color,fg=self.fg_color,font=("arial",35,"bold")).pack()
        btns=["Dashboard","Employee","Supplier","Category","Products","Sales","Exit"]
        self.btn_img= Image.open("images\\btn.png")
        self.btn_img =  ImageTk.PhotoImage(self.btn_img)
        btn_nr = -1
        for btn in btns:
            btn_nr += 1
            self.button=Button(button_frame,image=self.btn_img,anchor=W,compound=LEFT,text='      '+btn,font=("arial",17,"bold"),command=lambda x=btn_nr: self.Activate(x),cursor='hand2',bg=self.fg_color,bd=2,relief=RIDGE)
            self.button.pack(fill=X,pady=5)
            if btn_nr==0:
                self.button.config(bg="yellow",image=None)

        footer_lbl=Label(self.root,text="Welcome to Inventery management Project \n",bg="black",fg=self.fg_color,font=("arial",14,"bold")).pack(side=BOTTOM,fill=X)
        self.Activate(0)
        self.update_time()
    def Activate(self,token):
        try:
            self.Activate_Frame.destroy()
        except:
            pass
        self.Activate_Frame=Frame(self.root,bg=self.bg_color)
        if token==0:
            Speak_thread("Inventery dashboard")
            self.Activate_Frame.place(x=270,y=125,width=1090,height=568)
            Dashboard_obj=Dashboard(self.Activate_Frame)  
        elif token==1:
            Speak_thread("Entering Employee tab")
            self.Activate_Frame.place(x=270,y=125,width=1090,height=568)
            self.Employee_obj=Employee(self.Activate_Frame)
        elif token==2:
            Speak_thread("Entering supplier tab")
            self.Activate_Frame.place(x=270,y=125,width=1090,height=568)
            self.Supplier_obj=Supplier(self.Activate_Frame)
        elif token==3:
            Speak_thread("Entering category tab")
            self.Activate_Frame.place(x=270,y=125,width=1090,height=568)
            self.Category_obj=Category(self.Activate_Frame)
        elif token==4:
            Speak_thread("Entering product tab")
            self.Activate_Frame.place(x=270,y=125,width=1090,height=568)
            self.Product_obj=Product(self.Activate_Frame)
        elif token==5:
            Speak_thread("Entering sale tab")
            self.Activate_Frame.place(x=270,y=125,width=1090,height=568)
            self.Sale_obj=Sale(self.Activate_Frame)

        else:
            self.root.destroy()
            os.system('login.py')
    def update_time(self):
        time_=str(time.strftime('%I:%M:%S'))
        date_=str(time.strftime('%d/%m/%y'))
        self.clock_lbl.config(text=f"Inventery management system\t\tDate:- {date_}\t\tTime:-{time_}")
        self.clock_lbl.after(200,self.update_time)



if __name__ == '__main__':
    root=Tk()
    Inv=Inventery(root)
    root.mainloop()
