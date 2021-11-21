from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import  mysql.connector as mysql




class login_form:
	def __init__(self,root):
		self.root=root
		self.root.title("Login")
		root.geometry("15500x800+0+0")
		self.img = PhotoImage(file="icon/we.png")
		self.panel = Label(self.root, image=self.img)
		self.panel.pack()

		self.phone = StringVar()
		self.passwords =StringVar()

		frame = Frame(self.root,bg="black")
		frame.place(x=520,y=170,width=340,height=450)

		img1 = Image.open(r'icon/user.png')
		img1 = img1.resize((80,80), Image.ANTIALIAS)
		self.Photoimage1 = ImageTk.PhotoImage(img1)
		lable_img = Label(image=self.Photoimage1,bg="black",borderwidth=0)
		lable_img.place(x=640,y=170,width=100,height=100)

		company_name = Label(frame, text="E-Gas", font=("times new roman",20,"bold"),fg="white",bg="black")
		company_name.place(x=95,y=100)

		#label
		username_lb = Label(frame,text="Phone Number", font=("times new roman",15,"bold"),fg="white",bg="black")
		username_lb.place(x=70, y=150)

		self.usernametxt = Entry(frame,textvariable=self.phone,font=("times new roman",15,"bold"))
		self.usernametxt.place(x=40,y=180,width=270)

		password_lb = Label(frame, text="Password", font=("times new roman", 15, "bold"), fg="white", bg="black")
		password_lb.place(x=70, y=215)

		self.passwordtxt = Entry(frame,textvariable=self.passwords, font=("times new roman", 15, "bold"))
		self.passwordtxt.place(x=40, y=250, width=270)



		##############icon image ######################

		img2 = Image.open(r'icon/user.png')
		img2 = img2.resize((25, 25), Image.ANTIALIAS)
		self.Photoimage2 = ImageTk.PhotoImage(img2)
		lable_img2 = Label(image=self.Photoimage2, bg="black", borderwidth=0)
		lable_img2.place(x=570, y=323, width=25, height=25)

		img3 = Image.open(r'icon/user.png')
		img3 = img3.resize((25, 25), Image.ANTIALIAS)
		self.Photoimage3 = ImageTk.PhotoImage(img3)
		lable_img3 = Label(image=self.Photoimage3, bg="black", borderwidth=0)
		lable_img3.place(x=570, y=390, width=25, height=25)



		#login btn
		loginbtn = Button(frame, text="Login", command=self.Login, font=("times new roman", 15, "bold"), fg="white",bd=3,relief=RIDGE, bg="red", activeforeground="red",)
		loginbtn.place(x=110,y=320,width=120,height=35)
			#register btn
		regbtn = Button(frame, text="New User Registration", command=lambda:self.switch_frame(), font=("times new roman", 10, "bold"), borderwidth=0,fg="white",
						  bg="black", activeforeground="black", activebackground="red" )
		regbtn.place(x=20, y=370, width=120, height=35)

		forgetbtn = Button(frame, text="Forget Password", font=("times new roman", 10, "bold"), borderwidth=0, fg="white",
						  bg="black", activeforeground="black", activebackground="red" )
		forgetbtn.place(x=20, y=410, width=120, height=35)

	def register_window(self):
		self.new_window =Toplevel(self.root)
		self.app=Register(self.new_window)

	def switch_frame(self):
		self.root.destroy()
		import registration


	def Login(self):
		conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
		my_conn = conn.cursor()
		my_conn.execute("select * from user_tb where phone=%s and password= %s",(self.phone.get(),self.passwords.get()))
		row = my_conn.fetchone()
		if row==None:
			messagebox.showerror("Error","Phone number and Password is incorrect")
		else:
			if row[4] == 'Administrator':
				#messagebox.showinfo("Success", "Successfully Login",parent=self.root)
				self.root.destroy()
				import admin
			if row[4] == "Sale Person":
			   #messagebox.showinfo("Success", "Successfully Login",parent=self.root)
			   self.root.destroy()
			   import userdash
			
				#messagebox.showerror("user role error","You have role please meet the Admin")






root = Tk()
obj = login_form(root)
root.mainloop()




