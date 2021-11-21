from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import random
import pymysql
from tkinter import messagebox
import db_connect
import  mysql.connector as mysql
class Settings:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System Develop by Moxieus Tech.")
        self.root.config(bg="white")
        self.root.focus_force()
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()

        title = Label(self.root, text="Add/Edit Product",bd=1,relief=RIDGE,font=("times new roman",15,"bold")).place(x=0,y=0,width=1000)
        self.demandfrom = StringVar()
        self.priceperkg = StringVar()
        self.Id = StringVar()



        manager_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        manager_frame.place(x=2,y=40,width=400,height=580)

        m_title = Label(manager_frame,text="Add Product",bg="#009688",fg='white',font=("times new roman",15,"bold"))
        m_title.grid(row=0,columnspan=2,pady=10)

        lbl_itname = Label(manager_frame,text="Price/KG:",bg="#009688",fg='white',font=("times new roman",14,"bold"))
        lbl_itname.grid(row=1,column=0,pady=10,sticky="w")

        txt_itname = Entry(manager_frame,textvariable=self.priceperkg,font=("times new roman",14,"bold"),bd=2,relief=RIDGE)
        txt_itname.grid(row=1,column=1,pady=10,padx=20,sticky='w')

        lbl_costprice = Label(manager_frame, text="Demand from", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_costprice.grid(row=2, column=0, pady=10,padx=20, sticky="w")

        txt_costprice = Entry(manager_frame, textvariable=self.demandfrom, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        txt_costprice.grid(row=2, column=1, pady=10, padx=20, sticky='w')

        txt_id = Entry(manager_frame, textvariable=self.Id, font=("times new roman", 14, "bold"), bd=5,
                             relief=GROOVE)


        btn_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        btn_frame.place(x=15,y=350,width=380)

        #add_btn = Button(btn_frame,command=lambda:self.add_user(),text="Add",width=6).grid(row=0,column=0,padx=10,pady=10)
        add_btn = Button(btn_frame, text="Update",command=lambda:self.update(),width=10).grid(row=0, column=1, padx=10, pady=10)
        #add_btn = Button(btn_frame,command=lambda:self.Delete_data(),text="Delete", width=10).grid(row=0, column=2, padx=10, pady=10)
        add_btn = Button(btn_frame, command=lambda:self.clear(), text="Clear", width=10).grid(row=0, column=3, padx=10, pady=10)
        detail_frame = Frame(self.root,bd=3,relief=RIDGE,bg='#009688')
        detail_frame.place(x=420,y=40,width=670,height=500)


        table_frame = Frame(detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=10,y=70,width=760,height=500)

        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.userTable = ttk.Treeview(table_frame,columns=('s/n',"sale_to","priceperkg"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)

        self.userTable.heading("s/n", text="S/N")
        self.userTable.heading("sale_to", text="Demand From")
        self.userTable.heading("priceperkg", text="Price/KG")
        self.userTable['show'] = 'headings'
        self.userTable.column("s/n", width=10, anchor='n')
        self.userTable.column("sale_to", width=50,anchor='n')
        self.userTable.column("priceperkg", width=50,anchor='n')

        self.userTable.pack(fill=BOTH,expand=1)
        self.userTable.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    def add_user(self):
        conn =pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()

        my_conn.execute("insert into product_tb(p_name,costprice,salesprice,qty,remark,bar_code) values(%s,%s,%s,%s,%s,%s)", (
                                                                                                                self.itemname.get(),
                                                                                                                self.costprice.get(),
                                                                                                                self.salesprice.get(),
                                                                                                                self.qty.get(),
                                                                                                                self.remark.get(),
                                                                                                                self.barcode,
                                                                                                            ))

        conn.commit()
        self.fetch_data()
        self.clear()
        conn.close()

    def fetch_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from Gas_pricing")
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=row)
            conn.commit()
        conn.close()
    def clear(self):
        self.demandfrom.set('')
        self.priceperkg.set('')
        self.Id.set('')
    def get_cursor(self,ev):
        cursor_row = self.userTable.focus()
        contents= self.userTable.item(cursor_row)
        row=contents['values']
        print(row)
        self.demandfrom.set(row[1])
        self.priceperkg.set(row[2])
        self.Id.set(row[0])
    def update(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("update gas_pricing set sale_to=%s,price_per_kg=%s where id=%s", (
                                                                                                                        self.demandfrom.get(),
                                                                                                                        self.priceperkg.get(),

                                                                                                                        self.Id.get(),
                                                                                                                    ))

        conn.commit()
        self.fetch_data()
        self.clear()
        conn.close()
    def Delete_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("delete from product_tb where id=%s",self.Id.get())
        conn.commit()
        self.fetch_data()
        self.clear()

    def search_data(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from product_tb where "+str(self.search_by.get())+" like "+"'%"+str(self.search_txt.get()+"%'"))
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=row)
            conn.commit()
        conn.close()





if __name__ == "__main__":
    root = Tk()
    obj =Settings(root)
    root.mainloop()