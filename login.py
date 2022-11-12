from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3 as sq
import os
import time
import smtplib
import threading
import json
class login_page:
	def __init__(self, master):
		f = open('settings.json',)
		data = json.load(f)
		self.bg_color=data['bg']
		self.fg_color=data['fg']
		self.root=master
		self.root.geometry('900x550+200+80')
		self.root.title("Inventery Management System | Login")
		self.root.iconbitmap('images\\employee.ico')
		self.root.resizable(False, False)
		self.User_id=StringVar()
		self.User_pass=StringVar()
		self.User_otp=StringVar()
		self.new_pass=StringVar()
		self.con_pass_var=StringVar()
		self.Otp=''


		self.bg_img = Image.open('images\\img1.jpg')
		self.bg_img=self.bg_img.resize((900,550), Image.ANTIALIAS)
		width, height = self.bg_img.size
		self.bg_img = ImageTk.PhotoImage(self.bg_img)       
		        
		self.canvas = Canvas(self.root,bd=5,relief=RIDGE, highlightthickness=0)
		self.canvas.pack(fill=BOTH, expand=True)
		self.login_win()
	def login_win(self):
		self.canvas.create_image(0, 0, image=self.bg_img, anchor='nw')

		login_frame=Frame(self.root,bg=self.bg_color,bd=3,relief=GROOVE,width=585,height=400)
		self.canvas.create_window(160, 70, anchor="nw", window=login_frame)

		label = Label(self.root, text="Login Page",width=24,bd=2,relief=RIDGE, font=("Ariel 30 bold"), bg='gray', fg='white')
		self.canvas.create_window(162, 70, anchor="nw", window=label)

		user_label = Label(self.root, text="Employee Id", font=("Ariel 17 bold"),bg=self.bg_color,fg='white')
		self.canvas.create_window(230, 180, anchor="nw", window=user_label)


		password_label = Label(self.root, text="Password", font=("Ariel 17 bold"),bg=self.bg_color,fg='white')
		self.canvas.create_window(230, 240, anchor="nw", window=password_label)

		user_entry = Entry(self.root,textvar=self.User_id,bd=2,relief=GROOVE, font=("Ariel 15"))
		user_entry.focus()
		self.canvas.create_window(400, 185, anchor="nw", window=user_entry)

		
		password_entry = Entry(self.root,bd=2,relief=GROOVE, textvar=self.User_pass, font=("Ariel 15 bold"), show="*")
		self.canvas.create_window(400, 240, anchor="nw", window=password_entry)

		login_btn = Button(self.root, text="Log In",bd=3,relief=RIDGE, font=("Ariel 15 bold"),cursor='hand2',width=32, bg='black', fg='gray',command=self.login_auth)
		self.canvas.create_window(230, 290, anchor="nw", window=login_btn)

		or_label = Label(self.root, text="_"*78,bg=self.bg_color,fg='gray')
		self.canvas.create_window(230, 350, anchor="nw", window=or_label)

		forget_btn = Button(self.root,command=self.forget_panel, text="Reset Password ?",bd=0,font=("Ariel 15"),cursor='hand2',activebackground=self.bg_color,activeforeground="orange", bg=self.bg_color, fg='white')
		self.canvas.create_window(230, 400, anchor="nw", window=forget_btn)
	def forget_panel(self):
		conn=sq.connect(database=r'IMS.db')
		cur=conn.cursor()

		if self.User_id.get()=="":
			messagebox.showinfo('Empty','Please Enter Employee Id for Forget Password')
		else:
			cur.execute('select Email from Employee where Emp_id=?',(self.User_id.get(),))
			email=cur.fetchone()
			if email==None:
				messagebox.showerror('Empty','Invalid Employee id,Try again')
			else:
				self.canvas.delete(ALL)
				x = threading.Thread(target=self.send_mail, args=(email[0],))
				x.start()
				self.canvas.create_image(0, 0, image=self.bg_img, anchor='nw')
				login_frame=Frame(self.root,bg=self.bg_color,bd=3,relief=GROOVE,width=410,height=400)
				self.canvas.create_window(230, 70, anchor="nw", window=login_frame)
				label = Label(self.root, text="Forget Password",width=20,bd=2,relief=RIDGE, font=("Ariel 25 bold"), bg='gray', fg='white')
				self.canvas.create_window(232, 70, anchor="nw", window=label)
				mail_lbl = Label(self.root,background=self.bg_color,fg='white',text=f"Enter OTP send to your registered Email",bd=0, font=("Ariel 15 "),state='normal')
				self.canvas.create_window(260, 140, anchor="nw", window=mail_lbl)
				otp_entry = Entry(self.root,bd=2,relief=GROOVE, textvar=self.User_otp, font=("Ariel 15 bold"))
				self.canvas.create_window(260, 180, anchor="nw", window=otp_entry)
				confirm_btn = Button(self.root, text="Confirm",bd=2,relief=RIDGE, font=("Ariel 13 bold"),cursor='hand2',width=8, bg=self.bg_color, fg='white',command=self.validation)
				self.canvas.create_window(500, 180, anchor="nw", window=confirm_btn)

				pass_lbl = Label(self.root,background=self.bg_color,fg='white',text="New Password",bd=0, font=("Ariel 15 "),state='normal')
				self.canvas.create_window(260, 240, anchor="nw", window=pass_lbl)
				pass_entry = Entry(self.root,bd=2,relief=GROOVE, textvar=self.new_pass, font=("Ariel 15 bold"))
				self.canvas.create_window(260, 280, anchor="nw", window=pass_entry)
				con_pass = Label(self.root,background=self.bg_color,fg='white', text=f"Confirm Password",bd=0, font=("Ariel 15 "),state='normal')
				self.canvas.create_window(260, 330, anchor="nw", window=con_pass)
				con_pass_entry = Entry(self.root,bd=2,relief=GROOVE, textvar=self.con_pass_var, font=("Ariel 15 bold"))
				self.canvas.create_window(260, 370, anchor="nw", window=con_pass_entry)
				self.change_btn = Button(self.root, text="Submit",bd=2,relief=RIDGE,state='disabled', font=("Ariel 13 bold"),cursor='hand2',width=22, bg=self.bg_color, fg='white',command=self.update_pass)
				self.canvas.create_window(260, 420, anchor="nw", window=self.change_btn)
				change_btn = Button(self.root, text="Back to login ?",bd=0 ,font=("Ariel 13 bold"),cursor='hand2', bg=self.bg_color, fg='white',activebackground=self.bg_color,activeforeground='orange',command=self.login_win)
				self.canvas.create_window(500, 420, anchor="nw", window=change_btn)


				#forget_frame=Frame(self.root,bg=self.bg_color,bd=3,relief=GROOVE,width=585,height=400)
				#self.canvas.create_window(160, 70, anchor="nw", window=forget_frame)

	def login_auth(self):
		conn=sq.connect(database=r'IMS.db')
		cur=conn.cursor()
		if self.User_id.get()=="":
			messagebox.showinfo("Login System", "Please enter the Username")
		elif self.User_pass.get()=="":
			messagebox.showinfo("Login System", "Please enter the Password")
		elif self.User_id.get()=="" and self.User_pass.get()=="":
			messagebox.showinfo("Login System", "Please enter the Username and Password")
		else:
			try:
				cur.execute('select Emp_type from Employee where Emp_id=? and Password=?',(self.User_id.get(),self.User_pass.get()))
				user=cur.fetchone()
				if user==None:
					messagebox.showerror('Invalid','Invalid Username or Password')
				else:
					self.root.destroy()
					if user[0]=='Admin':
						os.system('main.py')
					else:
						os.system('billing.py')
			except Exception as e:
				messagebox.showerror('Error',e)
	def send_mail(self,to):
		self.Otp=int(time.strftime('%H%M%S'))+int(time.strftime('%d%m%y'))
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		server.login('chouhanvishal273@gmail.com','jiqruamhvpktnvzk')
		subj='Inventery Management System OTP'
		msg=f'Dear Sir/Madam Your Reset Otp is {str(self.Otp)}.\n\nWith Regards,\nIMS Team'
		msg='Subject:{}\n\n{}'.format(subj,msg)
		print(msg,self.Otp)
		server.sendmail('chouhanvishal273@gmail.com',to,msg)
		chk=server.ehlo()
		if chk[0]==250:
			print('yes')
			self.User_otp.set(self.Otp)
		else:
			print('no')
		#server.close()
 
	def validation(self):
		if self.Otp==int(self.User_otp.get()):
			print('success')
			self.change_btn.config(state='normal')
		else:
			messagebox.showinfo('Invalid','Please Enter valid Otp')
	def update_pass(self):
		conn=sq.connect(database=r'IMS.db')
		cur=conn.cursor()
		if self.new_pass.get()=="" or self.con_pass_var.get()=='':
			messagebox.showinfo('Empty','Please Enter Password')
		elif self.new_pass.get()!=self.con_pass_var.get():
			messagebox.showinfo('Empty','Please Enter Same Password')
		else:
			cur.execute("update Employee set Password=? where Emp_id=?",(self.new_pass.get(),self.User_id.get()))
			conn.commit()
			messagebox.showinfo('success','Password updated sucessfully')
		
if __name__ == '__main__':
    root=Tk()
    login=login_page(root)
    root.mainloop()
