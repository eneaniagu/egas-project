from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import random
import pymysql
from tkinter import messagebox
import db_connect
import  mysql.connector as mysql
class Supplier:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System Develop by Moxieus Tech.")
        self.root.config(bg="white")
        self.root.focus_force()
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()

        title = Label(self.root, text="Add user Form",bd=1,relief=RIDGE,font=("times new roman",15,"bold")).place(x=0,y=0,width=1000)
        self.fname = StringVar()
        self.lname = StringVar()
        self.phone = StringVar()
        self.password = StringVar()
        self.userROle = StringVar()
        self.Id = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()

        manager_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        manager_frame.place(x=2,y=40,width=400,height=580)

        m_title = Label(manager_frame,text="Add user",bg="#009688",fg='white',font=("times new roman",15,"bold"))
        m_title.grid(row=0,columnspan=2,pady=10)

        lbl_fname = Label(manager_frame,text="First Name",bg="#009688",fg='white',font=("times new roman",14,"bold"))
        lbl_fname.grid(row=1,column=0,pady=10,sticky="w")

        txt_fname = Entry(manager_frame,textvariable=self.fname,font=("times new roman",14,"bold"),bd=2,relief=RIDGE)
        txt_fname.grid(row=1,column=1,pady=10,padx=20,sticky='w')

        lbl_last = Label(manager_frame, text="last Name", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_last.grid(row=2, column=0, pady=10,padx=20, sticky="w")

        txt_last = Entry(manager_frame, textvariable=self.lname, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        txt_last.grid(row=2, column=1, pady=10, padx=20, sticky='w')

        lbl_phone = Label(manager_frame, text="Phone", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_phone.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        txt_phone = Entry(manager_frame,textvariable=self.phone, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        txt_phone.grid(row=3, column=1, pady=10, padx=20, sticky='w')


        lbl_role = Label(manager_frame, text="Role", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_role.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        role_combo = ttk.Combobox(manager_frame,textvariable=self.userROle,state='readonly', justify=CENTER,font=("time new roman", 12,))
        role_combo['values'] = ('Select role','Admin','Sale person')
        role_combo.grid(row=4, column=1, pady=10, padx=20, sticky='w')
        role_combo.current(0)


        lbl_password = Label(manager_frame, text="Password", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_password.grid(row=5, column=0, pady=10, padx=20, sticky="w")

        txt_password = Entry(manager_frame,textvariable=self.password, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        txt_password.grid(row=5, column=1, pady=10, padx=20, sticky='w')



        txt_id = Entry(manager_frame, textvariable=self.Id, font=("times new roman", 14, "bold"), bd=5,
                             relief=GROOVE)


        btn_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        btn_frame.place(x=15,y=350,width=380)

        add_btn = Button(btn_frame,command=lambda:self.add_user(),text="Add",width=6).grid(row=0,column=0,padx=10,pady=10)
        add_btn = Button(btn_frame, text="Update",command=lambda:self.update(),width=10).grid(row=0, column=1, padx=10, pady=10)
        add_btn = Button(btn_frame,command=lambda:self.Delete_data(),text="Delete", width=10).grid(row=0, column=2, padx=10, pady=10)
        add_btn = Button(btn_frame, command=lambda:self.clear(), text="Clear", width=10).grid(row=0, column=3, padx=10, pady=10)
        detail_frame = Frame(self.root,bd=3,relief=RIDGE,bg='#009688')
        detail_frame.place(x=420,y=40,width=670,height=500)

        # lbl_search= Label(detail_frame,text="Search by",font=("time new roman",14, 'bold'),bg='#009688',fg='white')
        # lbl_search.grid(row=0,column=0,pady=10,padx=0,sticky='w')
        combo_search= ttk.Combobox(detail_frame,textvariable=self.search_by,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_search['values'] = ("Search by","firstname","phone","lastname")
        combo_search.grid(row=0,column=0,padx=20,pady=10)
        combo_search.current(0)

        txt_search = Entry(detail_frame,textvariable=self.search_txt,width=20,font=("time new roman",14,'bold'),bd=5, relief=RIDGE)
        txt_search.grid(row=0,column=1,pady=10,padx=20,sticky='w')

        Button(detail_frame,  text="Search", command=lambda:self.search_data(),width=10,pady=5).grid(row=0, column=2, padx=10, pady=10)
        Button(detail_frame, text="Show All", command=lambda:self.fetch_data(),width=10,pady=5).grid(row=0, column=5, padx=10, pady=10)


        table_frame = Frame(detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=10,y=70,width=760,height=500)

        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.userTable = ttk.Treeview(table_frame,columns=('S/n',"firstname","lastname","phone","role","password"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)

        self.userTable.heading("S/n", text="S/N")
        self.userTable.heading("firstname", text="firstname")
        self.userTable.heading("lastname", text="lastname")
        self.userTable.heading("phone", text="phone")
        self.userTable.heading("password", text="password")
        self.userTable.heading("role", text="role")
        self.userTable['show'] = 'headings'
        self.userTable.column("S/n", width=50, anchor='w')
        self.userTable.column("firstname", width=100,anchor='w')
        self.userTable.column("lastname", width=100,anchor='w')
        self.userTable.column("phone", width=100,anchor='w')
        self.userTable.column("password", width=100, anchor='w')
        self.userTable.column("role", width=100,anchor='w')
        self.userTable.pack(fill=BOTH,expand=1)
        self.userTable.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    def add_user(self):
        conn =pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()

        my_conn.execute("insert into user_tb(firstname,lastname,phone,password,status) values(%s,%s,%s,%s,%s)", (
                                                                                                                self.fname.get(),
                                                                                                                self.lname.get(),
                                                                                                                self.phone.get(),
                                                                                                                self.password.get(),
                                                                                                                self.userROle.get(),
                                                                                                            ))
        print(my_conn)
        conn.commit()
        self.fetch_data()
        self.clear()
        conn.close()

    def fetch_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from user_tb")
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=row)
            conn.commit()
        conn.close()
    def clear(self):
        self.fname.set('')
        self.lname.set('')
        self.phone.set('')
        self.userROle.set('')
        self.password.set('')
        self.Id.set('')
    def get_cursor(self,ev):
        cursor_row = self.userTable.focus()
        contents= self.userTable.item(cursor_row)
        row=contents['values']
        self.fname.set(row[1])
        self.lname.set(row[2])
        self.phone.set(row[3])
        self.userROle.set(row[4])
        self.password.set(row[5])
        self.Id.set(row[0])
    def update(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("update user_tb set firstname=%s,lastname=%s,phone=%s,password=%s,status=%s where id=%s", (
                                                                                                                    self.fname.get(),
                                                                                                                    self.lname.get(),
                                                                                                                    self.phone.get(),
                                                                                                                    self.password.get(),
                                                                                                                    self.userROle.get(),
                                                                                                                    self.Id.get(),
                                                                                                                ))
        print(my_conn)
        conn.commit()
        self.fetch_data()
        self.clear()
        conn.close()
    def Delete_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("delete from user_tb where id=%s",self.Id.get())
        conn.commit()
        self.fetch_data()
        self.clear()

    def search_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from user_tb where "+str(self.search_by.get())+" like "+"'%"+str(self.search_txt.get()+"%'"))
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=row)
            conn.commit()
        conn.close()





if __name__ == "__main__":
    root = Tk()
    obj = Supplier(root)
    root.mainloop()