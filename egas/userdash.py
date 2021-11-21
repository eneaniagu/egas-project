from tkinter import *
import math
from add_produ import AddProduct
from adduser import AddUser
from settings import Settings
from invoice import Invoice
from expenses import Expenses
from supplier import Supplier
from sales import Sales
from PIL import Image, ImageTk
from tkinter import ttk
import os
import json
import random
from datetime import date
import time
from tkinter import messagebox
import mysql
import  mysql.connector as mysql
import os, sys
from win32printing import Printer

class UserDash:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Admin Dashboard")
        self.root.config(bg="white")
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()
        self.id = StringVar()
        self.search_txt = StringVar()
        self.itemname = StringVar()
        self.qty        = StringVar()
        self.Id         = StringVar()
        self.qty_want        = StringVar()
        self.gas_mode_payment = StringVar()
        self.items_mode_payment = StringVar()
      

        self.productName    = []
        self.productQty     = []
        self.receiptobj =   []
        self.productPrice   = []
        self.totalPrice     = []
        self.Ids            = []
        self.Qtys           = []
        # for empty list 
        self.link_list      = []
        self.link_listfor_gas =[]
        self.pricePer_Kg    = []
        self.No_of_kg     = [] 
        self.tatalgasprice = []

        #Gas Selling entries
        self.customer = StringVar()
        self.kg       = StringVar()
        self.today = time.strftime("%Y-%m-%d")
       

        

        conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()      
        my_conn.execute("select id from invoice_tb order by id desc")
        receipt = my_conn.fetchone()
        self.receipt_id =  receipt[0] + 1
       

        # ===== title ========#
        self.icon_title = PhotoImage(file="icon/lg2.png")
        title = Label(self.root, text="Dashboard | Cashier", image=self.icon_title, compound=LEFT, bg="#010c48",
                      fg="white", anchor="w", padx=20, font=("times new roman", 40, "bold"))
        title.place(x=0, y=0, relwidth=1, height=70)

        # ==== butonlogout =====#
        btn_logout = Button(self.root,command=self.logout, text="LOGOUT", cursor="hand2", font=("times new roman", 15, "bold"), bg="yellow")
        btn_logout.place(x=1170, y=10, height=30, width=150)

        topmenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        topmenu.place(x=0,y=70,relwidth=1,height=40)

        self.leftbtn_icon = PhotoImage(file="icon/ar.png")

        Button(topmenu, text="Sales",  command=self.sales, image=self.leftbtn_icon, compound=LEFT, padx=5,
                           anchor='n', cursor="hand2", bd=3, font=("times new roman", 15, "bold"), bg="White").grid(row=0,column=0,padx=10,pady=0)
        Button(topmenu, text="Expenses", command=self.expenses, image=self.leftbtn_icon, compound=LEFT, padx=5,
                           anchor='n', cursor="hand2", bd=3, font=("times new roman", 15, "bold"), bg="White").grid(row=0, column=1, padx=10,
                                                                                       pady=0)
        add_btn = Button(topmenu,text="Invoice", command=self.invoice, image=self.leftbtn_icon, compound=LEFT, padx=5,
                           anchor='n', cursor="hand2", bd=3, font=("times new roman", 15, "bold"), bg="White").grid(row=0, column=2,
                                                                                                      padx=10, pady=0)
        add_btn = Button(topmenu, text="Report", image=self.leftbtn_icon, compound=LEFT, padx=5,
                           anchor='s', cursor="hand2", bd=3, font=("times new roman", 15, "bold"), bg="White").grid(row=0, column=3, padx=10,
                                                                                               pady=0)




        # ====== body content =======#
        gas_frame = Frame(self.root,bd=2, relief=RIDGE, bg="white")
        gas_frame.place(x=10, y=120, width=600, height=2000)
        self.sale_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.sale_frame.place(x=615, y=120, width=730, height=2000)
        self.label_product = Label(gas_frame, text="Gas Selling", bd=2, relief=RIDGE, bg="#33bbf9", fg="white",
                                   font=("goudy old style", 20, "bold")).place(x=50, y=0, height=50, width=300)







        lbl_role = Label(gas_frame, text="Enter number of KG", bg="#009688", fg='white',
                          font=("times new roman", 14, "bold"))
        lbl_role.place(x=10,y=140,width=280,height=50)

        role_combo = Entry(gas_frame,textvariable=self.kg, justify=CENTER,bd=2, relief=RIDGE,font=("time new roman", 12,))
        role_combo.place(x=10,y=180,height=50,width=280)
    
        txt_phone = Entry(gas_frame, textvariable="self.phone", font=("times new roman", 14, "bold"), bd=2,
                          relief=RIDGE)
        # txt_phone.place(x=20,y=260)
        lbl_role = Label(gas_frame, text="What type of customer", bg="#009688", fg='white',
                         font=("times new roman", 14, "bold"))
        lbl_role.place(x=10, y=240, width=280, height=50)
        use_combo = ttk.Combobox(gas_frame, textvariable=self.customer, state='readonly', justify=CENTER,
                                  font=("time new roman", 12,))
        use_combo['values'] = ('Consumers', 'Dealers')
        use_combo.place(x=10, y=280, height=40, width=280)
        use_combo.current(0)
        
        lbl_payment = Label(gas_frame, text="Mode of Payment", bg="#009688", fg='white',
                         font=("times new roman", 14, "bold"))
        lbl_payment.place(x=10, y=330, width=280, height=50)
        payment_combo = ttk.Combobox(gas_frame, textvariable=self.gas_mode_payment, state='readonly', justify=CENTER,
                                  font=("time new roman", 12,))
        payment_combo['values'] = ('Cash', 'Transfer', "Pos")
        payment_combo.place(x=10, y=380, height=40, width=280)
        payment_combo.current(0)
                          
        
        Button(gas_frame, text="Add to list", command=lambda:self.Sale_gas(), width=6).place(x=20,y=440,height=40,width=80)
        Button(gas_frame, text="Print", command=lambda:self.gas_billing(), width=10).place(x=120,y=440,width=60,height=40)
        Button(gas_frame, text="Clear", command=lambda:self.ClearGasdata(), width=10).place(x=190,y=440,width=60,height=40)
    #============ RECEIPT FORMATING ===========================================#
        self.recipt_frame = Frame(gas_frame,bd=2, relief=RIDGE, bg="white")
        self.recipt_frame.place(x=295, y=120, width=300, height=350)
        
        # self.receiptframing = Frame(self.root)
        # self.receiptframing.place(x=0,y=0,width=300, height=300)
        # company = Label(self.receiptframing,text="e-Gas",bd=1,relief=RIDGE,font=("times new roman",15,"bold"))
        # company.pack()
    #================================ end =============================================#

         # gas selling receipt frame
        productname = Label(self.recipt_frame,text="Product", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        productname.place(x=10, y=20)
        productqty = Label(self.recipt_frame,text="Qty[kg]", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        productqty.place(x=120, y=20)
        productunitprice = Label(self.recipt_frame,text="Price/Unit", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        productunitprice.place(x=200, y=20)

        self.typeG = Label(self.recipt_frame, text="",bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
        self.typeG.place(x=50,y=250)
        self.totalG = Label(self.recipt_frame, text="" ,bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
        self.totalG.place(x=130,y=280) 



        # item sellings

        self.label_sales = Label(self.sale_frame, text="Items Selling", bd=2, relief=RIDGE, bg="#33bbf9", fg="white",
                                 font=("times new roman", 20, "bold")).place(x=50, y=0)

        self.insideframe = Frame(self.sale_frame,bd=2,relief=RIDGE, bg="white")
        self.insideframe.place(x=5,y=80,width=340,height=400)
            # search entry and button 
        sale_drop = ttk.Entry(self.insideframe, textvariable=self.search_txt, justify=CENTER,font=("time new roman", 12,))
        sale_drop.place(x=5, y=10, height=30, width=250)


       
       
        ttk.Entry(self.sale_frame, justify=CENTER, textvariable=self.Id,
                                 font=("time new roman", 12,))
         #search sale tree view                         
        treeview = Frame(self.insideframe,bd=2,relief=RIDGE, bg="white")
        treeview.place(x=2,y=45,width=335,height=400)




        Button(self.sale_frame, command=lambda: self.addtolist(), text="Add to list", width=6).place(x=20,y=420,height=40,width=80)
        Button(self.sale_frame, text="Print", command=lambda:self.generate_bill(), width=10).place(x=120,y=420,width=70,height=40)
        Button(self.sale_frame, text="Clear", command=lambda:self.ClearItemdata(), width=10).place(x=200,y=420,width=70,height=40)

        self.itemsList_frame = Frame(self.sale_frame, bd=2, relief=RIDGE, bg="white")
        self.itemsList_frame.place(x=350, y=80, width=370, height=400)
      
        productname = Label(self.itemsList_frame,text="Product Name", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        productname.place(x=10, y=20)
        productqty = Label(self.itemsList_frame,text="Qty", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        productqty.place(x=150, y=20)
        productunitprice = Label(self.itemsList_frame,text="Price/Unit", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        productunitprice.place(x=200, y=20)
        productTotal = Label(self.itemsList_frame,text="Total", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        productTotal.place(x=290, y=20)
            ###  item description #########################
       
        self.totalP = Label(self.itemsList_frame,text="", bg="white", fg='black',
                        font=("times new roman", 12, "bold"))
        self.totalP.place(x=200, y=360) 
         # ===== Footer  =======  ##
        footer_label = Label(self.root,text="Inventory management system | Developed by Moxieus Technology\n for technical issue contact 07089184071",compound=LEFT, bg="#4d636d", fg="white", font=("times new roman", 12)).pack(side=BOTTOM,fill=X)

               
       
       
    # ================================= sidebar new windows ===================#
        treeview = Frame(self.insideframe,bd=2,relief=RIDGE, bg="white")
        treeview.place(x=2,y=45,width=335,height=200)

        scroll_x = Scrollbar(treeview,orient=HORIZONTAL)
        scroll_y = Scrollbar(treeview,orient=VERTICAL)
        self.userTable = ttk.Treeview(treeview,columns=('item',"qty","price"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.userTable.xview)
        scroll_y.config(command=self.userTable.yview)

        self.userTable.heading("item", text="Item")
        self.userTable.heading("qty", text="Qty")
        self.userTable.heading("price", text="Price")
        self.userTable['show'] = 'headings'
        self.userTable.column("item", width=70, anchor='n')
        self.userTable.column("qty", width=120,anchor='n')
        self.userTable.column("price", width=50, anchor='n')
        self.userTable.pack(fill=BOTH,expand=1)
        self.userTable.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    def fetch_data(self):
        conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from product_tb")
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=[row[2],row[6],row[4],row[3],row[1],row[0]])
                Button(self.insideframe, text="search", bg="#009688", fg='white', command=lambda:self.search_data(),
                         font=("times new roman", 14, "bold")).place(x=255, y=10, width=70, height=30)
           

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
        txt_lbl = Label(self.sale_frame, text="Quantity", bg="#009688", fg='white',
                        font=("times new roman", 14, "bold"))
        txt_lbl.place(x=10, y=340, width=90, height=30)
        self.qtyentry =ttk.Entry(self.sale_frame, justify=CENTER, textvariable=self.qty_want,
                                 font=("time new roman", 12,))
        self.qtyentry.place(x=90,y=340,width=60,height=30)
        self.qty_want.set("1")

        paym_lbl = Label(self.sale_frame, text="mode of Payment", bg="#009688", fg='white',
                        font=("times new roman", 14, "bold"))
        paym_lbl.place(x=10, y=380, width=150, height=30)
        paym_combo = ttk.Combobox(self.sale_frame, textvariable=self.items_mode_payment, state='readonly', justify=CENTER,font=("time new roman", 12,))
        paym_combo['values'] = ('Cash', 'Transfer', "Pos")
        paym_combo.place(x=158,y=380,width=100,height=30)
        paym_combo.current(0)
         #===== selected itemname ======== #####
        self.itementry =ttk.Entry(self.sale_frame, justify=CENTER, textvariable=self.itemname, state="readonly",
                                 font=("time new roman", 12,))
        self.itementry.place(x=180,y=340,width=160,height=30)
        #===== selected item id
        self.identry = ttk.Entry(self.sale_frame, justify=CENTER, textvariable=self.Id, state="readonly",
                                 font=("time new roman", 12,))
        self.itemname.set(row[0]) 
        self.Id.set(row[5])

        conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from product_tb where id=%s and p_name= %s",(row[5],row[0]))
        result = my_conn.fetchone()
    
        self.Pname = result[2]
        self.Qty   = result[6]
        self.Price  = result[4]
        self.IDs     = result[0]
    def search_data(self):
       
        conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        my_conn.execute("select * from product_tb where p_name like "+"'%"+str(self.search_txt.get()+"%'"))
        rows = my_conn.fetchall()
        if len(rows)!=0:
            self.userTable.delete(*self.userTable.get_children())
            for row in rows:
                self.userTable.insert('',END,values=[row[1],row[2],row[6]])
                
            conn.commit()
            Button(self.insideframe, text="Back", bg="#009688", fg='white', command=lambda:self.fetch_data(),
                         font=("times new roman", 14, "bold")).place(x=255, y=10, width=70, height=30)
        conn.close()
    def addtolist(self):
           
            
            if int(self.qty_want.get()) > int(self.Qty):
                # delete entry when qty is above
                self.qtyentry.delete(0, 'end')
                self.itementry.delete(0, 'end')
                self.identry.delete(0, 'end')
                messagebox.showerror("Error","Your Resquest is out off Stock\n\t "+ self.Qty +" unit Left")
            else:
                total = (float(self.qty_want.get()) * float(self.Price))
                self.productName.append(self.Pname)
                self.productQty.append(self.Qty)
                self.productPrice.append(self.Price)
                self.totalPrice.append(total)
                self.Ids.append(self.IDs)
                self.Qtys.append(self.qty_want.get())
                #print(self.totalPrice)
                ok =1
                x = 0
                y_index = 60
                counter = 0
                for self.ro in self.productName:
                    self.productnamelist = Label(self.itemsList_frame, text=self.productName[counter],bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
                    self.productnamelist.place(x=10,y=y_index)

                    self.link_list.append(self.productnamelist)

                    self.qtylist = Label(self.itemsList_frame, text=self.Qtys[counter],bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
                    self.qtylist.place(x=150,y=y_index)

                    self.link_list.append(self.qtylist)

                    self.unitpricelist = Label(self.itemsList_frame, text=self.productPrice[counter],bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
                    self.unitpricelist.place(x=200,y=y_index)

                    self.link_list.append(self.unitpricelist)

                    self.totalunitprice = Label(self.itemsList_frame, text=self.totalPrice[counter],bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
                    self.totalunitprice.place(x=290,y=y_index)

                    self.link_list.append(self.totalunitprice)

                    y_index += 30
                    counter += 1


                self.totalP.config(text="Total : "+ str(sum(self.totalPrice)))
                
           
    def generate_bill(self):
            # generate transaction table for -each transaction did
        date = time.strftime("%Y-%m-%d")
        
        
            #printing to file 
        directory = "C:/Users/hp/egas/invoice/" + str(date) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        

        

        ## open file to write
        filname = str(random.randrange(5000, 10000)) 
        file_name = str(directory) + filname + '.txt'
        f = open(file_name, 'w')


            #receipt template
        font = {
        "height": 16,
        "margin":(0,9,2,3),
    }

        fonts = {
        "height": 6,
    }

        with Printer(linegap=1) as printer:
            printer.text("\t\t\t\t          e-Gas", font_config=font)
            printer.text("\t      e-24 gaz limited",font_config=fonts)
            printer.text(" 18 Upper Rehab Road\n       Emene, Enugu",font_config=fonts)
            printer.text("  Phone: 08021494749 \n  Email: e24gaz@gmail.com",font_config=fonts)
            printer.text("  Date: " + str(date) + "  "+ str(time.strftime("%I:%M%p")),font_config=fonts)
            printer.text("  Receipt No: "+str(self.receipt_id),font_config=fonts)
            printer.text("  Cashier: Ifeoma",font_config=fonts)
            printer.text("  Products    Qty        Amount") 
            d = 1
            ri = 0
            for t in self.productName:
                
                printer.text("  "+str(self.productName[ri])[:6]+"          "+str(self.Qtys[ri])+"         "+str(self.productPrice[ri])+"\n")
                ri +=1
                d +=1
            printer.text("                  Total : " + str(sum(self.totalPrice)) )
            printer.text("  Thanks For Your Patronage.") 
            printer.text("\n.  ") 
            printer.text("\n . ")  
            # second receipt ====== #
            printer.text("\t\t\t\t          e-Gas", font_config=font)
            printer.text("\t      e-24 gaz limited")
            printer.text(" 18 Upper Rehab Road\n       Emene, Enugu")
            printer.text("  Phone: 08021494749 \n  Email: e24gaz@gmail.com")
            printer.text("  Date: " + str(date) + "  "+ str(time.strftime("%I:%M%p")))
            printer.text("  Receipt No: "+str(self.receipt_id) )
            printer.text("  Cashier: Ifeoma" )
            printer.text("  Products    Qty        Amount") 
            d = 1
            ri = 0
            for t in self.productName:
                
                printer.text("  "+str(self.productName[ri])[:6]+"          "+str(self.Qtys[ri])+"         "+str(self.productPrice[ri])+"\n")
                ri +=1
                d +=1
            printer.text("                  Total : " + str(sum(self.totalPrice)) )
            printer.text("  Thanks For Your Patronage.") 
            printer.text("\n.  ") 
            printer.text("\n . ") 
             

        company1 = "\t\t\t\t\t e-Gas Company\n"
        min_company1  = "\t\t\t\t\t e-24 gaz Ltd\n"
        address1      = "\t\t\t\t 18 Upper Rehab Road Emene\n\t\t\t\t\t\t Enugu \n"
        phone1  =   "\t\t\t\t Phone: 08021494749 \n\t\t\t\t Email: e24gaz@gmail.com\n"
        dt1     =   "\t\t\t\t Date: " + str(date) + "\n"
        receiptno1 = "\t\t\t\t Receipt No: "+str(self.receipt_id)+ " \n\t\t\t\t Cashier: Ifeoma"
        table_header1 = "\n\t\t\t\tProducts\tQty\tAmount "
        final1 = company1 + min_company1 + address1 + phone1 +  "\n" + dt1 + receiptno1 + table_header1

        
        f.write(final1)

        # fill lable data
        d = 1
        ri = 0
        for t in self.productName:
            
            f.write("\n\t\t\t\t" + str(self.productName[ri])[:7] + ' \t'+str(self.Qtys[ri])+"\t"+str(self.productPrice[ri]) )
            ri +=1
            d +=1
        
        f.write("\n\n\t\t\t\t\t Total : " + str(sum(self.totalPrice)) + "\n")
        f.write("\t\t\t\t Thanks For Your Patronage.....")
        

       #os.startfile(file_name, "print")
        f.close()

        i = 0
        

        for ru in self.productName:
            initiate = "SELECT * FROM product_tb WHERE id='%s'"
            self.my_conn.execute(initiate,(self.Ids[i],))
            result =    self.my_conn.fetchall()
            for r in result:
                old_stock = r[6]
                new_stock = int(old_stock) - int(self.Qtys[i])
            #update table as items is been selectd 
                sql = "UPDATE product_tb SET qty='%s' WHERE id='%s'"
                self.my_conn.execute(sql,(new_stock,self.Ids[i]))
                self.conn.commit()
                self.fetch_data()
            ## insert transaction to transaction table
            query = "INSERT INTO transaction_tb(product_name,qty,amount,dt,paymentType,remark) values(%s,%s,%s,%s,%s,%s)"
            self.my_conn.execute(query,(self.productName[i],self.Qtys[i],self.productPrice[i],self.today,self.items_mode_payment.get(),"Item"))
            i +=1
            self.conn.commit()
        
            
        query = "INSERT INTO invoice_tb(name,invoice_from,remark,dt) values(%s,%s,%s,%s)"
        self.my_conn.execute(query,(filname,self.items_mode_payment.get(),"Item Sales",self.today))
        self.conn.commit()
        
        for b in self.link_list:
            b.destroy()
        del(self.productName[:])
        del(self.productQty[:]) 
        del(self.productPrice[:]) 
        del(self.totalPrice[:])    
        del(self.Ids[:])           
        del(self.Qtys[:])    
        self.totalP.config(text="")   
       
    def Sale_gas(self):

    
        initiate = "SELECT * FROM gas_pricing WHERE sale_to=%s"
        self.my_conn.execute(initiate,(self.customer.get(),))
        result =    self.my_conn.fetchone()
        self.pricePer_Kg.append(float(result[2]))
        self.No_of_kg.append(float(self.kg.get())) 
        pricePer_Kg = result[2]
       
        self.totalPrice =  sum(self.No_of_kg) * float(pricePer_Kg)
        
        self.customertypes = result[1]
        
        x = 0
        y_index = 50
        
       

        for self.ro in self.pricePer_Kg:

          # item list for gas selling
            self.product = Label(self.recipt_frame, text="Gas",bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
            self.product.place(x=10,y=y_index)
            self.link_listfor_gas.append(self.product)


            self.qty = Label(self.recipt_frame, text=self.No_of_kg[x],bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
            self.qty.place(x=120,y=y_index)
            self.link_listfor_gas.append(self.qty)


            self.unitprice = Label(self.recipt_frame, text=float(self.pricePer_Kg[x]),bg="white", fg='black',
                                font=("times new roman", 12, "bold"))
            self.unitprice.place(x=200,y=y_index)
            self.link_listfor_gas.append(self.unitprice)
            tot = self.pricePer_Kg[x] * self.No_of_kg[x] 
            self.tatalgasprice.append(tot)
            self.totalG.config(text="Total :"+ str(self.totalPrice))
            self.typeG.config(text="Customer Type: " + self.customertypes)
            

            y_index += 30
            x += 1
        
         

      

    def gas_billing(self):

        date = time.strftime("%Y-%m-%d")
        
            #printing to file 
        directory = "C:/Users/hp/egas/invoice/" + str(date) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

         ## open file to write
        filname = str(random.randrange(5000, 10000)) 
        file_name = str(directory) + filname + '.txt'
        f = open(file_name, 'w')

         #receipt template
        font = {
        "height": 16,
        "margin":(0,9,2,3),
    }
    

        with Printer(linegap=1) as printer:
            printer.text("\t\t\t\t          e-Gas", font_config=font)
            printer.text("\t      e-24 gaz limited")
            printer.text(" 18 Upper Rehab Road\n       Emene, Enugu")
            printer.text("  Phone: 08021494749 \n  Email: e24gaz@gmail.com")
            printer.text("  Date: " + str(date) + "  "+ str(time.strftime("%I:%M%p")))
            printer.text("  Receipt No: "+str(self.receipt_id) )
            printer.text("  Cashier: Ifeoma" )
            printer.text("  Products    Qty        Amount") 
            d = 1
            ri = 0
            for t in self.pricePer_Kg:
                
                printer.text("  "+"Gas"+"          "+str(self.No_of_kg[ri])+"kg"+"         "+str(self.pricePer_Kg[ri])+"\n")
                ri +=1
                d +=1
            printer.text("                  Total : " + str(self.totalPrice) )
            printer.text("  Thanks For Your Patronage.") 
            printer.text("\n.  ") 
            printer.text("\n . ")  
            # second receipt ====== #
            printer.text("\t\t\t\t          e-Gas", font_config=font)
            printer.text("\t      e-24 gaz limited")
            printer.text(" 18 Upper Rehab Road\n       Emene, Enugu")
            printer.text("  Phone: 08021494749 \n  Email: e24gaz@gmail.com")
            printer.text("  Date: " + str(date) + "  "+ str(time.strftime("%I:%M%p")))
            printer.text("  Receipt No: "+str(self.receipt_id) )
            printer.text("  Cashier: Ifeoma" )
            printer.text("  Products    Qty        Amount") 
            d = 1
            ri = 0
            
            for t in self.pricePer_Kg:
                
                printer.text("  "+"Gas"+"          "+str(self.No_of_kg[ri])+"kg"+"         "+str(self.pricePer_Kg[ri])+"\n")
                ri +=1
                d +=1
            printer.text("                  Total : " + str(self.totalPrice) )
            printer.text("  Thanks For Your Patronage.") 
            printer.text("\n.  ") 
            printer.text("\n . ") 
           
        

            #receipt template
        company = "\t e-Gas \n"
        min_company  = "\t\t e-24 gaz limited\n"
        address      = "\t\t\t\t 18 Upper Rehab Road Emene\n\t\t\t\t\t\t Enugu \n"
        phone  =   "\t\t\t\t Phone: 08021494749 \n\t\t\t\t Email: e24gaz@gmail.com\n"
        dt     =   "\t\t\t\t Date: " + str(date) + "\n"
        receiptno = "\t\t\t\t Receipt No: "+str(self.receipt_id)+" \n\t\t\t\t Cashier: Ifeoma"
        table_header = "\n\t\t\t\tProducts\t Qty  \tAmount "
        final = company + min_company + address + phone +  "\n" + dt + receiptno + table_header

       
        f.write(final)
        # fill lable data
        x=0
        for ru in self.pricePer_Kg:
            
            f.write("\n\t\t\t\t GAS \t\t" +str(self.No_of_kg[x])+"kg  \t"+str(self.pricePer_Kg[x]) )
            x +=1
        f.write("\n\n\t\t\t\t\t Total : " + str(self.totalPrice)  + "\n")
        f.write("\t\t\t\t Thanks For Your Patronage.....")
        f.write("\n\n\n\n\n")
        #second receipt 
        #os.startfile(file_name, "print")
        f.close()

        
        query = "INSERT INTO transaction_tb(product_name,qty,amount,paymentType,remark,dt) values(%s,%s,%s,%s,%s,%s)"
        self.my_conn.execute(query,("Gas",sum(self.No_of_kg),self.totalPrice,self.gas_mode_payment.get(),self.customertypes,self.today))
        self.conn.commit()
        query = "INSERT INTO invoice_tb(name,invoice_from,remark,dt) values(%s,%s,%s,%s)"
        self.my_conn.execute(query,(filname,self.gas_mode_payment.get(),self.customertypes,self.today))
        self.conn.commit()
        for b in self.link_listfor_gas:
            b.destroy()
        del(self.pricePer_Kg[:])
        del(self.No_of_kg[:])
        self.typeG.config(text="")
        self.totalG.config(text="")
    def ClearGasdata(self):

        for b in self.link_listfor_gas:
            b.destroy()
        del(self.pricePer_Kg[:])
        del(self.No_of_kg[:])
        self.typeG.config(text="")
        self.totalG.config(text="")
        
    
    def ClearItemdata(self):
        for b in self.link_list:
            b.destroy()
        del(self.productName[:])
        del(self.productQty[:]) 
        del(self.productPrice[:]) 
        del(self.totalPrice[:])    
        del(self.Ids[:])           
        del(self.Qtys[:])    
        self.totalP.config(text="")



        

        
            

###================================= sidebar new windows ===================#

    def addproduct(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = AddProduct(self.new_window)

    def adduser(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = AddUser(self.new_window)

    def settings(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = Settings(self.new_window)

    def expenses(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = Expenses(self.new_window)

    def sales(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = Sales(self.new_window)

    def supplier(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = Supplier(self.new_window)

   
    def invoice(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = Invoice(self.new_window)
    def logout(self):
        self.root.destroy()
        import login
   

root = Tk()
obj = UserDash(root)
root.mainloop()