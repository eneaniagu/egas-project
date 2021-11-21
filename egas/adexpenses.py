from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import random
import pymysql
import time
from tkinter import messagebox
import db_connect
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

        title = Label(self.root, text="Add/Edit Expenses",bd=1,relief=RIDGE,font=("times new roman",15,"bold")).place(x=0,y=0,width=1000)
        self.itemname = StringVar()
        self.costprice = StringVar()
        self.salesprice = StringVar()
        self.qty = StringVar()
        self.remark = StringVar()
        self.today = time.strftime("%Y-%m-%d")
        self.Id = StringVar()
        self.Toexp = []
        
        self.description = StringVar()
        self.amount = StringVar()
        digit = '12A34X5Y67Z89'
        alpha = digit+'0'
        self.barcode = 'R'+random.choice(digit) + ''.join(random.choice(alpha) for _ in range(9))


        #==== yrs sselection =======#

        self.yrs = StringVar()
        self.day = StringVar()
        self.months = StringVar()

        self.year = ["Year"]
        self.days = ["Day"]

        for dd in range(32):
            self.days.append(dd)
        for nu in range(11):
             self.year.append("202"+str(nu))
        


        self.manager_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        self.manager_frame.place(x=2,y=40,width=400,height=580)

        m_title = Label(self.manager_frame,text="Add Expenses",bg="#009688",fg='white',font=("times new roman",15,"bold"))
        m_title.grid(row=0,columnspan=2,pady=10)

       
        # lbl_costprice = Label(self.manager_frame, text="Description", bg="#009688", fg='white',
        #                   font=("times new roman", 14, "bold"))
        # lbl_costprice.grid(row=2, column=0, pady=10,padx=20, sticky="w")

        # txt_costprice = Entry(self.manager_frame, textvariable=self.description, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        # txt_costprice.grid(row=2, column=1, pady=10, padx=20, sticky='w')

        # lbl_saleprice = Label(self.manager_frame, text="Amount Spent", bg="#009688", fg='white',
        #                   font=("times new roman", 14, "bold"))
        # lbl_saleprice.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        # txt_saleprice = Entry(self.manager_frame,textvariable=self.amount, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        # txt_saleprice.grid(row=3, column=1, pady=10, padx=20, sticky='w')


        # txt_id = Entry(self.manager_frame, textvariable=self.Id, font=("times new roman", 14, "bold"), bd=5,
        #                      relief=GROOVE)

    #======== prevoius history =========#
    
        
       

       

      
        self.btn_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        self.btn_frame.place(x=15,y=350,width=380)

        #add_btn = Button(self.btn_frame,command=lambda:self.add_user(),text="Add",width=6).grid(row=0,column=0,padx=10,pady=10)
        #add_btn = Button(self.btn_frame, text="Add ",command=lambda:self.add_user(),width=10).grid(row=0, column=1, padx=10, pady=10)
        
        
         # view expenses 
        view_btn = Button(self.btn_frame, text="Previous",command=lambda:self.showPrev(),width=10).grid(row=0, column=3, padx=10, pady=10)
        
        


        detail_frame = Frame(self.root,bd=3,relief=RIDGE,bg='#009688')
        detail_frame.place(x=420,y=40,width=670,height=500)

        self.expTo = Label(self.root, text="",bd=1,relief=RIDGE,font=("times new roman",15,"bold"),bg='#009688',fg="white")
        self.expTo.place(x=540,y=450,width=280, height=50)
        


        table_frame = Frame(detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=10,y=20,width=650,height=380)

        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.userTable = ttk.Treeview(table_frame,columns=('s/n',"description","amount","date"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)

        self.userTable.heading("s/n", text="S/N")
        self.userTable.heading("description", text="Description")
        self.userTable.heading("amount", text="Amount")
        self.userTable.heading("date", text="Date")
        self.userTable['show'] = 'headings'
        self.userTable.column("s/n", width=50, anchor='n')
        self.userTable.column("description", width=100,anchor='n')
        self.userTable.column("amount", width=100,anchor='n')
        self.userTable.column("date", width=100,anchor='n')
        self.userTable.pack(fill=BOTH,expand=1)
        self.userTable.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    def add_user(self):
        conn =pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()

        my_conn.execute("insert into expenses_tb(description,amount,create_by,dt) values(%s,%s,%s,%s)", (self.description.get(),self.amount.get(),"Ifeoma",self.today))

        conn.commit()
        del(self.Toexp[:])
        self.fetch_data()
        self.check_history()
        self.clear()
        conn.close()

    def fetch_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from expenses_tb where dt=%s",(self.today),)
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            q=1
            for row in rows:
                self.userTable.insert('',END,values=[q,row[1],row[2],row[4]])
                self.Toexp.append(float(row[2]))
                q +=1
            conn.commit()
            self.expTo.config(text="Total Expenses: " + str(sum(self.Toexp)))
        else:
            self.userTable.insert('',END,'NO Record for today')
        conn.close()
    def clear(self):
        self.description.set('')
        self.amount.set('')
        self.Id.set('')
    def get_cursor(self,ev):
        cursor_row = self.userTable.focus()
        contents= self.userTable.item(cursor_row)
        row=contents['values']
        self.description.set(row[1])
        self.amount.set(row[2])
        self.Id.set(row[0])
    def update(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("update expenses_tb set description=%s,amount=%s where id=%s", (
                                                                                                                        self.description.get(),
                                                                                                                        self.amount.get(),
                                                                                                        
                                                                                                                        self.Id.get(),
                                                                                                                    ))

        conn.commit()
        del(self.Toexp[:])
        self.fetch_data()
        self.clear()
        conn.close()
    def check_history(self):
        
        if self.months.get() == "January":
             self.mont = '01'
        elif self.months.get() == "Feb":
            self.mont ="02"
        elif self.months.get() == "March":
            self.mont = "03"
        elif self.months.get() == "April" :
            self.mont ="04"
        elif self.months.get() == "May":
            self.mont = "05"
        elif self.months.get() == "June" :
            self.mont ="06"
        elif self.months.get() == "July":
            self.mont = "07"
        elif self.months.get() == "August" :
            self.mont = "08"
        elif self.months.get() == "Stepmber":
            self.mont = "09"
        elif self.months.get() == "October" :
            self.mont = '10'
        elif self.months.get() == "Novmber":
            self.mont = '11'
        elif self.months.get() == "December" :
            self.mont ="12"
        else:
            self.mont = "0"
        
            
        self.yr_s = self.yrs.get()+'-'+self.mont+'-'+self.day.get()
        
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from expenses_tb where dt=%s",(self.yr_s),)
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            q=1
            for row in rows:
                self.userTable.insert('',END,values=[q,row[1],row[2],row[4]])
                self.Toexp.append(float(row[2]))
                q +=1
            conn.commit()
            self.expTo.config(text="Total Expenses: " + str(sum(self.Toexp)))
        else:
            self.userTable.delete(* self.userTable.get_children())
            self.userTable.insert('',END,'NO Record for today')
            self.expTo.config(text="Total Expenses: [0]")
        conn.close()
    def showPrev(self):

        add_btn = Button(self.btn_frame, text="Check",command=lambda:self.check_history(),width=10).grid(row=0, column=2, padx=10, pady=10)
        
        combo_day= ttk.Combobox(self.manager_frame,textvariable=self.day,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_day['values'] = (self.days)
        combo_day.place(x=130,y=150,height=40,width=100)
        combo_day.current(0)

        

        combo_month= ttk.Combobox(self.manager_frame,textvariable=self.months,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_month['values'] = ("Month","January","Feb","March", "April","May","June","July","August","Stepmber","October","Novmber","December")
        combo_month.place(x=280,y=150,height=30,width=100)
        combo_month.current(0)

  
        combo_yrs= ttk.Combobox(self.manager_frame,textvariable=self.yrs,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_yrs['values'] = (self.year)
        combo_yrs.place(x=180,y=230,height=40,width=100)
        combo_yrs.current(0)




if __name__ == "__main__":
    root = Tk()
    obj = Expenses(root)
    root.mainloop()