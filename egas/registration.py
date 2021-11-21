from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import  mysql.connector as mysql


class Register:
    def __init__(self,root):
        self.root = root
        self.root.title("Registration")
        self.root.geometry("1600x900+0+0")

        #============== variable decaration=============#
        self.fname = StringVar()
        self.lname = StringVar()
        self.userRole = StringVar()
        self.phone = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()


######image #####
        self.img = PhotoImage(file="images/11.png")
        self.panel = Label(self.root, image=self.img)
        self.panel.place(x=0, y=0, relwidth=1, relheight=1)

        ###########imag 2
        self.img1 = PhotoImage(file="images/we.png")
        self.panel1 = Label(self.root, image=self.img1)
        self.panel1.place(x=50, y=100, width=470, height=550)

        #+============ main frame  =======#
        frame = Frame(self.root, bg="white")
        frame.place(x=520,y=100,width=800,height=550);

        register_lable = Label(frame,text="Registration", font=("times new roman",25,"bold"),fg="darkgreen",bg="white")
        register_lable.place(x=20, y=20)

    #======= Label and entry =================#
        fn_label = Label(frame, text="first Name",font=("times new roman",14,"bold"),fg="black",bg="white")
        fn_label.place(x=50, y=100)

        self.Fn_entry = ttk.Entry(frame,textvariable=self.fname, font=("times new roman", 13, "bold"))
        self.Fn_entry.place(x=40, y=130, width=300)

        ln_label = Label(frame, text="Last Name", font=("times new roman", 14, "bold"), fg="black", bg="white")
        ln_label.place(x=50, y=160)

        self.ln_entry = ttk.Entry(frame, textvariable=self.lname, font=("times new roman", 13,"bold"))
        self.ln_entry.place(x=40, y=185, width=300)

        num_label = Label(frame, text="Phone Number", font=("times new roman", 14, 'bold'), fg="black", bg="white")
        num_label.place(x=50, y=215)

        self.num_entry = ttk.Entry(frame,textvariable=self.phone, font=("times new roman", 13,"bold"))
        self.num_entry.place(x=40, y=240, width=300)

        password_label = Label(frame, text="Password", font=("times new roman", 14, "bold"), fg="black", bg="white")
        password_label.place(x=50, y=270)

        self.password_entry = ttk.Entry(frame,textvariable=self.password, font=("times new roman", 13, "bold"))
        self.password_entry.place(x=40, y=295, width=300)


        conf_pass_label = Label(frame, text="Confirm Password", font=("times new roman", 14,"bold"), fg="black", bg="white")
        conf_pass_label.place(x=50, y=325)

        self.conf_pass_entry = ttk.Entry(frame,textvariable=self.confirm_password, font=("times new roman", 13,"bold"))
        self.conf_pass_entry.place(x=40, y=360, width=300)

        self.user_role_lb = Label(frame, text="what's the role of user sigining in",
                                  font=("times new roman", 14, "bold"), fg="black", bg="white")
        self.user_role_lb.place(x=50, y=395)

        self.user_role_entry = ttk.Combobox(frame, textvariable=self.userRole,state='readonly', justify=CENTER,font=("time new roman", 12))
        self.user_role_entry["value"] = ("Select Role", "Admin", "Sale Person")
        self.user_role_entry.place(x=40, y=420, width=300)
        self.user_role_entry.current(0)

        self.submit_btn  = Button(frame, command=self.register, text="Register",font=("times new roman", 15,"bold") ,fg="white",
						  bg="red", activeforeground="black", activebackground="red" )
        self.submit_btn.place(x=70,y=460, width=100)

        self.login_btn = Button(frame, text="login",command=self.switch_frame,font=("times new roman", 15, "bold"), borderwidth=0, fg="red",
						  bg="white", activeforeground="black" )

        self.login_btn.place(x=200, y=460, width=100)


        #======================= function ==================================#

    def register(self):
        if self.fname.get() == "" or self.lname.get() == "" or self.phone.get() == "" or self.password.get() == "" or self.confirm_password == "" or self.userRole.get() == "":
            messagebox.showerror("Error", "All fields are Required")
        elif self.password.get() != self.confirm_password.get():
            messagebox.showerror("Error", "Password and Confrim password must be thr same!")
        else:
            conn = mysql.connect(host="localhost",user="root",password="",database="egas_db")

            my_conn = conn.cursor()
            phone = self.phone.get()

            query = ("select * from user_tb where phone=%s")
            value = (self.phone.get(),)
            my_conn.execute(query,value)
            row = my_conn.fetchone()
            if row!=None:
                messagebox.showerror("ERROR", "user Already exist, please try another phone number")
            else:

                my_conn.execute("insert into user_tb(firstname,lastname,phone,password,status) values(%s,%s,%s,%s,%s)",(
                                                                                    self.fname.get(),
                                                                                    self.lname.get(),
                                                                                    self.phone.get(),
                                                                                    self.password.get(),
                                                                                    self.userRole.get(),
                                                                                    ))
                
                conn.commit()
                conn.close()
                #messagebox.showinfo("SUCCESS", "REGISTRATION SUCCESSFULLY")
                self.root.destroy()
                import login
                
    def switch_frame(self):
        self.root.destroy()
        import login


root = Tk()
root.title("Registration")
Reg = Register(root)
root.mainloop()