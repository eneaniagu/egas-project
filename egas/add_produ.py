from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import random
import pymysql
from tkinter import messagebox
import db_connect
import  mysql.connector as mysql
class AddProduct:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System Develop by Moxieus Tech.")
        self.root.config(bg="white")
        self.root.focus_force()
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()

        title = Label(self.root, text="Add/Edit Product",bd=1,relief=RIDGE,font=("times new roman",15,"bold")).place(x=0,y=0,width=1000)
        self.itemname = StringVar()
        self.costprice = StringVar()
        self.salesprice = StringVar()
        self.qty = StringVar()
        self.remark = StringVar()
        self.Id = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        digit = '12A34X5Y67Z89'
        alpha = digit+'0'
        self.barcode = 'R'+random.choice(digit) + ''.join(random.choice(alpha) for _ in range(9))


        manager_frame = Frame(self.root,bd=3,relief=RIDGE,bg="#009688")
        manager_frame.place(x=2,y=40,width=400,height=580)

        m_title = Label(manager_frame,text="Add Product",bg="#009688",fg='white',font=("times new roman",15,"bold"))
        m_title.grid(row=0,columnspan=2,pady=10)

        lbl_itname = Label(manager_frame,text="name",bg="#009688",fg='white',font=("times new roman",14,"bold"))
        lbl_itname.grid(row=1,column=0,pady=10,sticky="w")

        txt_itname = Entry(manager_frame,textvariable=self.itemname,font=("times new roman",14,"bold"),bd=2,relief=RIDGE)
        txt_itname.grid(row=1,column=1,pady=10,padx=20,sticky='w')

        lbl_costprice = Label(manager_frame, text="cost price", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_costprice.grid(row=2, column=0, pady=10,padx=20, sticky="w")

        txt_costprice = Entry(manager_frame, textvariable=self.costprice, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        txt_costprice.grid(row=2, column=1, pady=10, padx=20, sticky='w')

        lbl_saleprice = Label(manager_frame, text="sales price", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_saleprice.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        txt_saleprice = Entry(manager_frame,textvariable=self.salesprice, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        txt_saleprice.grid(row=3, column=1, pady=10, padx=20, sticky='w')


        lbl_qty = Label(manager_frame, text="quantity", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_qty.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        txt_qty = Entry(manager_frame, textvariable=self.qty, font=("times new roman", 14, "bold"), bd=2,
                           relief=RIDGE)
        txt_qty.grid(row=4, column=1, pady=10, padx=20, sticky='w')



        # #lbl_password = Label(manager_frame, text="remark", bg="#009688", fg='white',
        #                   font=("times new roman", 14, "bold"))
        #lbl_password.grid(row=5, column=0, pady=10, padx=20, sticky="w")

        txt_remark = Entry(manager_frame,textvariable=self.remark, font=("times new roman", 14, "bold"), bd=2, relief=RIDGE)
        #txt_remark.grid(row=5, column=1, pady=10, padx=20, sticky='w')



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
        combo_search['values'] = ("Search by","bar_code","p_name","costprice")
        combo_search.grid(row=0,column=0,padx=20,pady=10)
        combo_search.current(0)

        txt_search = Entry(detail_frame,textvariable=self.search_txt,width=20,font=("time new roman",14,'bold'),bd=5, relief=RIDGE)
        txt_search.grid(row=0,column=1,pady=10,padx=20,sticky='w')

        Button(detail_frame,  text="Search", command=lambda:self.search_data(),width=10,pady=5).grid(row=0, column=2, padx=10, pady=10)
        Button(detail_frame, text="Show All", command=lambda:self.fetch_data(),width=10,pady=5).grid(row=0, column=5, padx=10, pady=10)


        table_frame = Frame(detail_frame, bd=4,relief=RIDGE,bg='#009688')
        table_frame.place(x=10,y=70,width=650,height=380)

        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        self.userTable = ttk.Treeview(table_frame,columns=('barcode',"items","costprice","salesprice","qty"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)

        self.userTable.heading("barcode", text="Ref No:")
        self.userTable.heading("items", text="items")
        self.userTable.heading("costprice", text="costprice")
        self.userTable.heading("salesprice", text="salesprice")
        self.userTable.heading("qty", text="qty")
        self.userTable['show'] = 'headings'
        self.userTable.column("barcode", width=50, anchor='n')
        self.userTable.column("items", width=100,anchor='n')
        self.userTable.column("costprice", width=100,anchor='n')
        self.userTable.column("salesprice", width=100,anchor='n')
        self.userTable.column("qty", width=100, anchor='n')
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
        my_conn.execute("select * from product_tb")
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=[row[0],row[2],row[3],row[4],row[6]])
            conn.commit()
        conn.close()
    def clear(self):
        self.itemname.set('')
        self.costprice.set('')
        self.salesprice.set('')
        self.qty.set('')
        self.remark.set('')
        self.Id.set('')
    def get_cursor(self,ev):
        cursor_row = self.userTable.focus()
        contents= self.userTable.item(cursor_row)
        row=contents['values']
        print(contents)
        print(row)
        self.itemname.set(row[1])
        self.costprice.set(row[2])
        self.salesprice.set(row[3])
        self.qty.set(row[4])
        self.Id.set(row[0])
    def update(self):
        conn = pymysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("update product_tb set p_name=%s,costprice=%s,salesprice=%s,qty=%s,remark=%s where id=%s", (
                                                                                                                        self.itemname.get(),
                                                                                                                        self.costprice.get(),
                                                                                                                        self.salesprice.get(),
                                                                                                                        self.qty.get(),
                                                                                                                        self.remark.get(),
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
    obj = AddProduct(root)
    root.mainloop()