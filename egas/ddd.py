from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import random
import time
import pymysql
from tkinter import messagebox
import  mysql.connector as mysql
class Expenses:
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
        self.description = StringVar()
        self.amount = StringVar()
        self.userROle = StringVar()
        self.Id = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.today = time.strftime("%Y-%m-%d")
        self.Toexp = []

        manager_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        manager_frame.place(x=2,y=40,width=400,height=580)

        m_title = Label(manager_frame,text="Add user",bg="#009688",fg='white',font=("times new roman",15,"bold"))
        m_title.grid(row=0,columnspan=2,pady=10)

        lbl_fname = Label(manager_frame,text="Description",bg="#009688",fg='white',font=("times new roman",14,"bold"))
        lbl_fname.grid(row=1,column=0,pady=10,sticky="w")

        txt_fname = Entry(manager_frame,textvariable=self.description,font=("times new roman",14,"bold"),bd=2,relief=RIDGE)
        txt_fname.place(x=120,y=60, width=250,height=30)


        lbl_password = Label(manager_frame, text="amount", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_password.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        txt_password = Entry(manager_frame,textvariable=self.amount, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        txt_password.grid(row=9, column=1, pady=10, padx=20, sticky='w')



        txt_id = Entry(manager_frame, textvariable=self.Id, font=("times new roman", 14, "bold"), bd=5,
                             relief=GROOVE)


        btn_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        btn_frame.place(x=15,y=350,width=380)

        add_btn = Button(btn_frame,command=lambda:self.add_expenses(),text="Add",width=6).grid(row=0,column=0,padx=10,pady=10)
        add_btn = Button(btn_frame, text="Update",command=lambda:self.update(),width=10).grid(row=0, column=1, padx=10, pady=10) 
        detail_frame = Frame(self.root,bd=3,relief=RIDGE,bg='#009688')
        detail_frame.place(x=420,y=40,width=670,height=500)

        # lbl_search= Label(detail_frame,text="Search by",font=("time new roman",14, 'bold'),bg='#009688',fg='white')
      

        txt_search = Label(detail_frame,textvariable="-Expenses-",width=20,font=("time new roman",14,'bold'),bd=1,)
        txt_search.grid(row=0,column=1,pady=10,padx=20,sticky='w')
        
        self.expTo = Label(self.root, text="",bd=1,relief=RIDGE,font=("times new roman",15,"bold"),bg='#009688',fg="white")
        self.expTo.place(x=540,y=430,width=280, height=50)

        

        table_frame = Frame(detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=10,y=70,width=650,height=300)

        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.userTable = ttk.Treeview(table_frame,columns=("amount","description","date"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)


        self.userTable.heading("amount", text="Amount")
        self.userTable.heading("description", text="Description")
        self.userTable.heading("date", text="Date")
        self.userTable['show'] = 'headings'
        self.userTable.column("amount", width=50,anchor='n')
        self.userTable.column("description", width=100,anchor='n')
        self.userTable.column("date", width=50,anchor='n')
        self.userTable.pack(fill=BOTH,expand=1)
        self.userTable.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    def add_expenses(self):
        # conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        # my_conn = conn.cursor(buffered=True)
        # my_conn.execute("insert into expenses_tb(description,amount,create_by,dt) values(%s,%s,%s,%s)",(
        #                                                                             self.description.get(),
        #                                                                             self.amount.get(),
        #                                                                             "Ifeoma",
        #                                                                             self.today,
                                                                                    
        #                                                                             ))
                
        
        # conn.commit()
        
        query = "INSERT INTO expenses_tb(description,amount,create_by,dt) values(%s,%s,%s,%s)"
        self.my_conn.execute(query,(self.description.get(),self.amount.get(),"Ifeoma",self.today))
        self.conn.commit()
        self.clear()
        # self.conn.close()

    def fetch_data(self):
        
        self.my_conn.execute("select * from expenses_tb where dt=%s and create_by= %s",(self.today,"abuchi"))
        rows = self.my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            nu = 1
            for row in rows:
                self.Toexp.append(float(row[2]))
                self.userTable.insert('',END,values=[row[2],row[1],row[4],row[0]])
                nu +=1
            self.conn.commit()
            self.expTo.config(text="Total Expenses: " + str(sum(self.Toexp)))
        self.conn.close()
    def clear(self):
        self.description.set('')
        self.amount.set('')
        self.Id.set('')
    def get_cursor(self,ev):
        cursor_row = self.userTable.focus()
        contents= self.userTable.item(cursor_row)
        row=contents['values']
      
        self.amount.set(row[1])
        self.description.set(row[0])
        self.Id.set(row[3])
    def update(self):
        
        self.my_conn.execute("update expenses_tb set description=%s,amount=%s where id=%s", (
                                                                                                                    self.description.get(),
                                                                                                                    self.amount.get(),
                                                                                                                    self.Id.get(),
                                                                                                                   
                                                                                                                ))
        
        self.conn.commit()
        self.fetch_data()
        self.clear()
        self.conn.close()
   

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
    obj = Expenses(root)
    root.mainloop()