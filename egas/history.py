from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import random
import pymysql
from tkinter import messagebox
import time
import db_connect
import  mysql.connector as mysql
class History:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System Develop by Moxieus Tech.")
        self.root.config(bg="white")
        self.root.focus_force()
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()

        title = Label(self.root, text="History Records",bd=1,relief=RIDGE,font=("times new roman",15,"bold")).place(x=0,y=0,width=1000)
        self.fname = StringVar()
        self.lname = StringVar()
        self.phone = StringVar()
        self.password = StringVar()
        self.userROle = StringVar()
        self.yrs = StringVar()
        self.day = StringVar()
        self.months = StringVar()

        year = ["Year"]
        day = ["Day"]

        self.today = time.strftime("%Y-%m-%d")
        self.totalsales = []
        self.totalKg = []
        self.totalcash = []
        self.totalexpenses = []
        self.totalTransfer = []
        self.totalPos    = []
     
        for dd in range(32):
            day.append(dd)
        for nu in range(11):
             year.append("202"+str(nu))


        self.manager_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        self.manager_frame.place(x=2,y=40,width=260,height=580)

        m_title = Label(self.manager_frame,text="Histories",bg="#009688",fg='white',font=("times new roman",15,"bold"))
        m_title.grid(row=0,columnspan=2,pady=10)

        lbl_day= Label(self.manager_frame,text="Day:",font=("time new roman",12, 'bold'),bg='#009688',fg='white')
        lbl_day.place(x=5,y=60,height=50,width=100)
        combo_day= ttk.Combobox(self.manager_frame,textvariable=self.day,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_day['values'] = (day)
        combo_day.place(x=5,y=100,height=50,width=100)
        combo_day.current(0)

        lbl_month= Label(self.manager_frame,text="Month",font=("time new roman",12, 'bold'),bg='#009688',fg='white')
        lbl_month.place(x=130,y=60,height=50,width=100)
        combo_month= ttk.Combobox(self.manager_frame,textvariable=self.months,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_month['values'] = ("Month","January","Feb","March", "April","May","June","July","August","Stepmber","October","Novmber","December")
        combo_month.place(x=130,y=100,height=50,width=100)
        combo_month.current(0)

        lbl_yrs= Label(self.manager_frame,text="Year",font=("time new roman",12, 'bold'),bg='#009688',fg='white')
        lbl_yrs.place(x=60,y=150,height=50,width=100)
        combo_yrs= ttk.Combobox(self.manager_frame,textvariable=self.yrs,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        combo_yrs['values'] = (year)
        combo_yrs.place(x=60,y=190,height=50,width=100)
        combo_yrs.current(0)

        self.add_btn = Button(self.manager_frame, text="Check History",command=lambda:self.get_history(),width=10)
        self.add_btn.place(x=40,y=250,height=50,width=150)
       


        # lbl_yrs= Label(self.manager_frame,text="Year",font=("time new roman",12, 'bold'),bg='#009688',fg='white')
        # lbl_yrs.place(x=60,y=150,height=50,width=100)
        # combo_yrs= ttk.Combobox(self.manager_frame,textvariable=self.search_by,width=10,state='readonly', justify=CENTER,font=("time new roman",12))
        # combo_yrs['values'] = ("Search by","firstname","phone","lastname")
        # combo_yrs.place(x=60,y=190,height=50,width=100)
        # combo_yrs.current(0)

        # add_btn = Button(self.manager_frame, text="Add ",command=lambda:self.add_user(),width=10).place(x=45,y=250,height=50,width=150)




       

        detail_frame = Frame(self.root,bd=3,relief=RIDGE,bg='#009688')
        detail_frame.place(x=280,y=40,width=780,height=500)

        


        table_frame = Frame(detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=10,y=70,width=760,height=500)
        ####  result Lable list #############
        self.label_total = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_total.place(x=5,y=20,height=80,width=240)

        self.label_exp = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_exp.place(x=250,y=20,height=80,width=240)

        self.label_cash = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_cash .place(x=500,y=20,height=80,width=240)

        ##second row
        self.label_dealers = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_dealers.place(x=5,y=120,height=80,width=240)

        self.label_consumer = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_consumer.place(x=250,y=120,height=80,width=240)

        self.label_kg = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_kg .place(x=500,y=120,height=80,width=240)
       ## thrid row 
        self.label_trnf = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_trnf.place(x=5,y=220,height=80,width=240)

        self.label_pos = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_pos.place(x=250,y=220,height=80,width=240)

        self.label_bal = Label(table_frame, text="\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",16,"bold"))
        self.label_bal .place(x=500,y=220,height=80,width=240)
       

    def get_history(self):

        
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
    
        self.add_btn.config(text="")
        self.add_btn2 = Button(self.manager_frame, text="Back",command=lambda:self.clear(),width=10)
        self.add_btn2.place(x=40,y=250,height=50,width=150)
        #====== check if list is empty then set the text zero =============#
        # if len(self.totalsales) == 0:
        #     self.label_total.config(text="Total Sales\n[zero]")
        #     print(self.totalsales)
        # else:

            ## ========= for total sale =============== #
        self.my_conn.execute("select * from transaction_tb where dt=%s",(self.yr_s,))
        resul =self.my_conn.fetchall()
        for row in resul:
            self.totalsales.append(float(row[3]))
        
        self.label_total.config(text="Total Sales\n[#"+str(sum(self.totalsales)) +"]")
        self.conn.commit()

         ## ========= for total Expense =============== #

        self.my_conn.execute("select * from expenses_tb where dt=%s",(self.yr_s,))
        resu =self.my_conn.fetchall()
        for ro in resu:
            self.totalexpenses.append(float(ro[2]))
    
        self.label_exp.config(text="Total Expenses\n[#"+str(sum(self.totalexpenses)) +"]")
        self.conn.commit()

         ## ========= for total cash =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and paymentType=%s",(self.yr_s,"Cash"))
        result =self.my_conn.fetchall()
        
        for ri in result:
            self.totalcash.append(float(ri[3]))

        self.label_cash.config(text="Total Cash\n[#"+str(sum(self.totalcash)) +"]")
        self.conn.commit()


        ## ========= for total invoice =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and product_name=%s",(self.yr_s,"Gas"))
        re =self.my_conn.fetchall()
        
        for ni in re:
            self.totalKg.append(float(ni[2]))
    
        self.label_kg.config(text="Total kg Sold \n["+str(sum(self.totalKg)) +"kg]")
        self.conn.commit()

         ## ========= for total pos =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and paymentType=%s",(self.yr_s,"Pos"))
        tel =self.my_conn.fetchall()
        
        for nl in tel:
            self.totalPos.append(float(nl[3]))
    
        self.label_pos.config(text="Total Pos  \n[#"+str(sum(self.totalPos)) +"]")
        self.conn.commit()

        ## ========= for total Transfer =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and paymentType=%s",(self.yr_s,"Transfer"))
        Fo =self.my_conn.fetchall()
        po = []
        for lo in Fo:
            po.append(float(lo[3]))
           
            self.totalTransfer.append(float(lo[3]))
            
        self.label_trnf.config(text="Total Transfer \n[#"+str(sum(self.totalTransfer)) +"]")
        self.conn.commit()

        ## ========= for total exavalut sell for the day =============== #
        tpsale = sum(self.totalcash)
        texp = sum(self.totalexpenses)
        unspend_cash = tpsale - texp
        self.label_bal.config(text="Remaining Bal Exp \n[#"+str(unspend_cash) +"]")


        ## ========= for total present count =============== #

        self.my_conn.execute("select * from invoice_tb where dt=%s and remark=%s",(self.yr_s,"Dealers"))
        reu = self.my_conn.fetchall()
    
        
    
        self.label_dealers.config(text="Present No of Dealers \n["+str(self.my_conn.rowcount)+"]")
        self.conn.commit()


         ## ========= for total constumer present count =============== #

        self.my_conn.execute("select * from invoice_tb where dt=%s and remark=%s",(self.yr_s,"Consumers"))
        reu = self.my_conn.fetchall()
        
        
    
        self.label_consumer.config(text="Present No of Consumer \n["+str(self.my_conn.rowcount)+"]")
        self.conn.commit()

    def clear(self):
        self.add_btn2.config(text="")
        self.add_btn = Button(self.manager_frame, text="Check History",command=lambda:self.get_history(),width=10)
        self.add_btn.place(x=40,y=250,height=50,width=150)
        

        del(self.totalsales[:])
        del(self.totalKg[:])
        del(self.totalcash[:])
        del(self.totalexpenses[:])
        del(self.totalTransfer[:])
        del(self.totalPos[:])

        
        self.label_total.config(text="[0]")
        self.label_exp.config(text="[0]")

        self.label_cash.config(text="[0]")
        self.label_dealers.config(text="[0]")
        self.label_consumer.config(text="[0]")
        self.label_kg.config(text="[0]")
        self.label_trnf.config(text="[0]")
        self.label_pos.config(text="[0]")
        self.label_bal.config(text="[0]")



if __name__ == "__main__":
    root = Tk()
    obj = History(root)
    root.mainloop()