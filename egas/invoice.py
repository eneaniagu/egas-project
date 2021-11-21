from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import time
import random
import pymysql
from tkinter import messagebox
import db_connect
import  mysql.connector as mysql
class Invoice:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System Develop by Moxieus Tech.")
        self.root.config(bg="white")
        self.root.focus_force()
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()

        title = Label(self.root, text="Invoice",bd=1,relief=RIDGE,font=("times new roman",15,"bold")).place(x=0,y=0,width=1000)
        self.fname = StringVar()
        self.lname = StringVar()
        self.phone = StringVar()
        self.password = StringVar()
        self.userROle = StringVar()
        self.Id = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.today = time.strftime("%Y-%m-%d")

        



       
        detail_frame = Frame(self.root,bd=3,relief=RIDGE,bg='#009688')
        detail_frame.place(x=20,y=40,width=870,height=500)

       

        txt_search = Label(detail_frame,textvariable="Invoice",bg='#009688',fg="white",width=20,font=("time new roman",14,'bold'),bd=1,)
        txt_search.grid(row=0,column=1,pady=10,padx=20,sticky='w')

     

        table_frame = Frame(detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=10,y=70,width=760,height=500)

        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.userTable = ttk.Treeview(table_frame,columns=('S/n',"invoice NO","for","description"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)

        self.userTable.heading("S/n", text="S/N")
        self.userTable.heading("invoice NO", text="Invoice NO")
        self.userTable.heading("for", text="For")
        self.userTable.heading("description", text="Description")
        self.userTable['show'] = 'headings'
        self.userTable.column("S/n", width=50, anchor='n')
        self.userTable.column("invoice NO", width=100,anchor='n')
        self.userTable.column("for", width=100,anchor='n')
        self.userTable.column("description", width=100,anchor='n')
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
        
        initiate = "SELECT * FROM invoice_tb WHERE dt=%s"
        self.my_conn.execute(initiate,(self.today,))
        rows = self.my_conn.fetchall()
        nu = 1
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=[nu,row[0],row[2],row[3]])
                nu +=1
            self.conn.commit()
        self.conn.close()
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
    obj = Invoice(root)
    root.mainloop()