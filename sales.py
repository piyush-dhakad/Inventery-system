from  tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk,messagebox
import os
import json
class Sale:
    def __init__(self, master):
        
        f = open('settings.json',)
        data = json.load(f)
        self.bg_color=data['bg']
        self.fg_color=data['fg']
        self.root=master
        self.searchtxt=StringVar()
        self.img1= Image.open("images\\inv3.jpg")
        self.img1=self.img1.resize((430,440),Image.ANTIALIAS)
        self.img1 =  ImageTk.PhotoImage(self.img1)

        self.bill_list=[]

        intro_lbl=Label(self.root,text="Customer Bill Reports",bg="gray",fg="white",font=("time new roman",30,"bold")).place(x=50,y=20,width=1000)

        search_frame=Frame(self.root,bg=self.bg_color)
        search_frame.place(x=50,y=100,width=550,height=75)

        Name_entry=Entry(search_frame,textvariable=self.searchtxt,font=("time new roman",15,"bold"),bg='white')
        Name_entry.place(x=130,y=10,width=150,height=30)
        Name_entry.bind("<Return>",self.search)
        intro_lbl=Label(search_frame,text="Bill Name",bg=self.bg_color,fg="white",font=("time new roman",15,"bold")).place(x=10,y=10)

        search_btn=Button(search_frame,command=self.search,text="Search",font=("time new roman",13,"bold"),bg='black',fg='white',cursor='hand2').place(x=300,y=8,width=120)
        clear_btn=Button(search_frame,command=self.clear,text="Clear",font=("time new roman",13,"bold"),bg='black',fg='white',cursor='hand2').place(x=425,y=8,width=120)
    
        Detail_frame=Frame(self.root,bd=3,relief=RIDGE,bg=self.bg_color)
        Detail_frame.place(x=50,y=160,width=150,height=400)

        scrolly=Scrollbar(Detail_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)

        self.sale_list=Listbox(Detail_frame,yscrollcommand=scrolly.set,font=('Bahnschrift 11',14), cursor="hand2", bd=0, activestyle="none", takefocus=False, selectmode="SINGLE",highlightthickness=0,selectbackground='darkorange',selectforeground='black',bg='white',fg='black')
        self.sale_list.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.sale_list.yview)

        show_frame=Frame(self.root,bd=3,relief=RIDGE,bg=self.bg_color)
        show_frame.place(x=205,y=160,width=390,height=400)
        intro_lbl=Label(show_frame,text="Customer Bill Area",bg="gray",fg=self.bg_color,font=("time new roman",25,"bold")).pack(fill=X)

        scrolly=Scrollbar(show_frame,orient=VERTICAL)
        scrolly.pack(fill=Y,side=RIGHT)

        self.sale_detail=Text(show_frame,yscrollcommand=scrolly.set,bg=self.bg_color,fg="white")
        self.sale_detail.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.sale_detail.yview)


        self.img1_lbl=Label(self.root,image=self.img1)
        self.img1_lbl.place(x=620,y=110)
        self.show()
        self.sale_list.bind("<Double-Button-1>",self.get_data)


    def search(self,event=None):
        if self.searchtxt.get()=="":
            messagebox.showerror("Error","Enter Invoice Name")
        else:
            if self.searchtxt.get() in self.bill_list:
                file=open("bill\\"+self.searchtxt.get()+'.txt','r')
                self.sale_detail.delete(1.0,END)
                for text in file:
                    self.sale_detail.insert(END,text)
                file.close()
                del self.bill_list[:]
                self.sale_list.delete(0,END) 
                self.bill_list.append(self.searchtxt.get())
                print(self.bill_list)
                for name in self.bill_list:
                    name=name.split('.')
                    print(name)
                    self.sale_list.insert(END,name)
            else:
                messagebox.showinfo("Error","Invoice Not found in list")



    def clear(self):
        self.searchtxt.set("")
        self.sale_list.delete(0,END) 
        self.show()
    def show(self):
        del self.bill_list[:]
        self.sale_list.delete(0,END) 
        list1=os.listdir('bill')
        for name in list1:
            name=name.split('.')
            if name[-1]=="txt":
                self.sale_list.insert(END,name[0])
                self.bill_list.append(name[0])

    def get_data(self,event):
        self.sale_detail.config(state='normal')
        index=self.sale_list.curselection()
        file_name=self.sale_list.get(index)+'.txt'
        file=open("bill\\"+file_name,'r')
        self.sale_detail.delete(1.0,END)
        for text in file:
            self.sale_detail.insert(END,text)
        file.close()
        self.sale_detail.config(state='disabled')

if __name__ == '__main__':
    root=Tk()
    Inv=Sale(root)
    root.mainloop()