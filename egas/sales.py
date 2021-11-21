from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import random
import pymysql
from tkinter import messagebox
import db_connect
import  mysql.connector as mysql
import time
class Sales:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System Develop by Moxieus Tech.")
        self.root.config(bg="white")
        self.root.focus_force()
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()

        title = Label(self.root, text="Sales",bd=1,relief=RIDGE,font=("times new roman",15,"bold")).place(x=0,y=0,width=1000)
        self.fname = StringVar()
        self.lname = StringVar()
        self.phone = StringVar()
        self.password = StringVar()
        self.userROle = StringVar()
        self.Id = StringVar()
        self.customertype = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.today = time.strftime("%Y-%m-%d")
        self.year = StringVar()
        self.days = StringVar()
        self.months = StringVar()
        self.sort_by_year = ['year']
        self.paymentType =  StringVar()
        self.SummonUP = []

   
    
        self.detail_frame = Frame(self.root,bd=3,relief=RIDGE,bg='#009688')
        self.detail_frame.place(x=10,y=40,width=1000,height=500)

        year = ["Select Year"]
        day = ["Select Day"]
     
        for dd in range(32):
            day.append(dd)
        for nu in range(11):
             year.append("202"+str(nu))
        

######### sort by year month and day
        Label(self.detail_frame,bd=2, relief=RIDGE,bg="white").place(x=5,y=10,width=300,height=135)
        Label(self.detail_frame,text="Sort by year,month & day", fg='black',
                        font=("times new roman", 12, "bold")).place(x=20,y=0,width=180,height=30)

        combo_year= ttk.Combobox(self.detail_frame,textvariable=self.year,width=20,height=200,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_year['values'] = year
        combo_year.place(x=10,y=50,width=100,height=30)
        combo_year.current(0)

        combo_month= ttk.Combobox(self.detail_frame,textvariable=self.months,width=20,height=200,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_month['values'] = ("Select Motnth","January","Feb","March", "April","May","June","July","August","Stepmber","October","Novmber","December")
        combo_month.place(x=150,y=50,width=100,height=30)
        combo_month.current(0)

        combo_day= ttk.Combobox(self.detail_frame,textvariable=self.days,width=20,height=200,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_day['values'] = day
        combo_day.place(x=10,y=90,width=100,height=30)
        combo_day.current(0)

        Button(self.detail_frame, command=lambda:self.sort_data_yrs(), text="Get Data", width=6, bg="#33bbf9",fg="white").place(x=160,y=100,height=40,width=100)

##########3  sort payment mode ##############################
        Label(self.detail_frame,bd=2, relief=RIDGE,bg="white").place(x=10,y=160,width=300,height=100)
        Label(self.detail_frame, text="Sort by Payment Mode",bg="white", fg='black',
                        font=("times new roman", 14, "bold")).place(x=20,y=160)
        opt= ttk.Combobox(self.detail_frame,textvariable=self.paymentType,width=20,height=200,state='readonly', justify=CENTER,font=("time new roman",12))
        opt['values'] = ["Cash","Transfer","Pos"]
        opt.place(x=20,y=200, width=100,height=50)
        opt.current(0)

        Button(self.detail_frame, text="Get Data",command=lambda:self.sort_data_paymentType(), width=6, bg="#33bbf9",fg="white").place(x=160,y=215,height=40,width=100)


        Label(self.detail_frame,bd=2, relief=RIDGE,bg="white").place(x=10,y=320,width=300,height=100)

        Label(self.detail_frame, text="Sort by customer Type",bg="white", fg='black',
                        font=("times new roman", 14, "bold")).place(x=20,y=310)
        opt= ttk.Combobox(self.detail_frame,textvariable=self.customertype,width=20,height=200,state='readonly', justify=CENTER,font=("time new roman",12))
        opt['values'] = ["Dealers","Consumers"]
        opt.place(x=20,y=350, width=100,height=50)
        opt.current(0)

        Button(self.detail_frame, text="Get Data", command=lambda:self.sort_by_customerType(), width=6, bg="#33bbf9",fg="white").place(x=160,y=360,height=40,width=100)
        
       

        # Button(self.detail_frame,  text="Check", command=lambda:self.search_data(),width=10,pady=5).grid(row=0, column=3, padx=10, pady=10)

        table_frame = Frame(self.detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=330,y=5,width=650,height=400)

     

        #Button(self.detail_frame, command=lambda:self.sumtotal(),text="Check Total", width=6, bg="#33bbf9",fg="white").place(x=550,y=410,height=40,width=100)
        self.totalP =Label(self.detail_frame, text='', width=6,font=("times new roman", 16, "bold"),bg='#009688',fg="white",bd=5)
        self.totalP.place(x=650,y=410,height=40,width=150)
        
        
        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.userTable = ttk.Treeview(table_frame,columns=('S/n',"items","quantities","price","remark","date"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)

        self.userTable.heading("S/n", text="Mode")
        self.userTable.heading("items", text="Items")
        self.userTable.heading("quantities", text="Quantity")
        self.userTable.heading("price", text="Price")
        self.userTable.heading("remark", text="Custumer")
        self.userTable.heading("date", text="Date")
        self.userTable['show'] = 'headings'
        self.userTable.column("S/n", width=50, anchor='n')
        self.userTable.column("items", width=100,anchor='n')
        self.userTable.column("quantities", width=100,anchor='n')
        self.userTable.column("price", width=100,anchor='n')
        self.userTable.column("remark", width=100, anchor='n')
        self.userTable.column("date", width=100, anchor='n')
        self.userTable.pack(fill=BOTH,expand=1)
        self.userTable.bind("<ButtonRelease-1>")
        self.fetch_data()
    

    def fetch_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from transaction_tb where dt=%s",(self.today,))
        rows = my_conn.fetchall()
    
        Q=0
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.SummonUP.append(float(row[3]))
                self.userTable.insert('',END,values=[row[4],row[1],row[2],row[3],row[5],row[6]])
               
                Q +=1
            self.conn.commit()
            Tp = sum(self.SummonUP)
            self.totalP.config(text="Total: " +str(Tp))
            del(self.SummonUP[:])
        
        
        else:
             self.userTable.insert('',END,'NO Record for today')
             del(self.SummonUP[:])
             self.totalP.config(text="")
        conn.close()

    def clear(self):
        self.fname.set('')
        self.lname.set('')
        self.phone.set('')
        self.userROle.set('')
        self.password.set('')
        self.Id.set('')


    def sort_data_yrs(self):
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
            
        self.yrs = self.year.get()+'-'+self.mont+'-'+self.days.get()
  
        initiate = "SELECT * FROM transaction_tb WHERE dt=%s" 
        self.my_conn.execute(initiate,(self.yrs,))
        rows =    self.my_conn.fetchall()
        Q=1
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.SummonUP.append(float(row[3]))
                self.userTable.insert('',END,values=[row[4],row[1],row[2],row[3],row[5],row[6]])
                Q +=1
            self.conn.commit()
            Tp = sum(self.SummonUP)
            del(self.SummonUP[:])
            self.totalP.config(text="Total: " +str(Tp))
        else:
             
            self.userTable.delete(* self.userTable.get_children())
            self.userTable.insert('',END,values=['NO Record'])
            del(self.SummonUP[:])
            self.totalP.config(text="")
            

        # self.my_conn.close()

    def sort_data_paymentType(self):
        
        
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
        
            
        self.yrs = self.year.get()+'-'+self.mont+'-'+self.days.get()

        initiate = "SELECT * FROM transaction_tb WHERE paymentType=%s and dt=%s" 
        self.my_conn.execute(initiate,(self.paymentType.get(),self.yrs))
        rows =    self.my_conn.fetchall()
        Q=0
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.SummonUP.append(float(row[3]))
                self.userTable.insert('',END,values=[row[4],row[1],row[2],row[3],row[5],row[6]])
                Q +=1
            self.conn.commit()
            Tp = sum(self.SummonUP)
            self.totalP.config(text="Total: " +str(Tp))
            del(self.SummonUP[:])
        
        else:
             
            self.userTable.delete(* self.userTable.get_children())
            self.userTable.insert('',END,values=['NO Record'])
            del(self.SummonUP[:])


    def sort_by_customerType(self):

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
            
        self.yrs = self.year.get()+'-'+self.mont+'-'+self.days.get()
        

        initiate = "SELECT * FROM transaction_tb WHERE remark=%s and %s" 
        self.my_conn.execute(initiate,(self.customertype.get(),self.yrs))
        rows =    self.my_conn.fetchall()
        
        Q=0
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.SummonUP.append(float(row[3]))
                self.userTable.insert('',END,values=[row[4],row[1],row[2],row[3],row[5],row[6]])
                Q +=1
            self.conn.commit()
            Tp = sum(self.SummonUP)
            self.totalP.config(text="Total: " +str(Tp))
            del(self.SummonUP[:])
        
        else:
             
            self.userTable.delete(* self.userTable.get_children())
            self.userTable.insert('',END,values=['NO Record'])
            del(self.SummonUP[:])

    def sumtotal(self):

        print(self.SummonUP)
        Tp = sum(self.SummonUP)
        print(Tp)
        del(self.SummonUP[:])




if __name__ == "__main__":
    root = Tk()
    obj = Sales(root)
    root.mainloop()