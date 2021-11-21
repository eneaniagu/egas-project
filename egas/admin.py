from tkinter import *
from add_produ import AddProduct
from adduser import AddUser
from settings import Settings
from invoice import Invoice
from history import History
from adexpenses import Expenses
from supplier import Supplier
import db_connect
import  mysql.connector as mysql
import time
from sales import Sales
from PIL import Image, ImageTk

class Admin:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Admin Dashboard")
        self.root.config(bg="white")
        self.conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        self.my_conn = self.conn.cursor()


        #====== variables =========================== ###
        self.today = time.strftime("%Y-%m-%d")
        self.totalsales = []
        self.totalKg = []
        self.totalcash = []
        self.totalexpenses = []
        self.totalTransfer = []
        self.totalPos    = []
        

        #===== title ========#
        self.icon_title = PhotoImage(file="icon/lg2.png")
        title = Label(self.root, text="Dashboard | admin",image=self.icon_title,compound=LEFT,bg="#010c48",fg="white", anchor="w",padx=20, font=("times new roman",40,"bold"))
        title.place(x=0,y=0,relwidth=1,height=70)

        #==== butonlogout =====#
        btn_logout = Button(self.root,command=self.logout,text="LOGOUT",cursor="hand2",font=("times new roman",15,"bold"), bg="yellow")
        btn_logout.place(x=1170,y=10,height=30,width=150)

        #===== clock ===== 
        dat = time.strftime("%d-%m-%Y")
        ti = time.strftime("%H:%M:%S")

        title = Label(self.root, text="Welcome inventory system\t\t Date: "+dat +"\t\t Time: "+ti,compound=LEFT,bg="#4d636d",fg="white", font=("times new roman",15))
        title.place(x=0,y=70,relwidth=1,height=30)

        #====== left menu ==============#
        self.leftMenu_logo = Image.open("icon/menu.png")
        self.leftMenu_logo=self.leftMenu_logo.resize((120,120),Image.ANTIALIAS)
        self.leftMenu_logo=ImageTk.PhotoImage(self.leftMenu_logo)

        leftMenu = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        leftMenu.place(x=0,y=102,width=200,height=565)

        left_labelLogo = Label(leftMenu,image=self.leftMenu_logo)
        left_labelLogo.pack(side=TOP,fill=X)

        #========= menu button ====# 
        title = Label(leftMenu, text="Something new",bg="#009688",fg="white", font=("times new roman",10)).pack(side=TOP,fill=X)

        self.leftbtn_icon = PhotoImage(file="icon/ar.png")

        btn_items = Button(leftMenu,text="Product",command=self.addproduct,image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_sales = Button(leftMenu,text="Sales",command=self.sales,image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_print = Button(leftMenu,text="User", command=self.adduser, image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_Settings = Button(leftMenu,command=self.settings,text="Settings",image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_expense = Button(leftMenu,text="Expenses",command=self.expenses,image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_exit = Button(leftMenu,text="History Records",command=self.history,image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_exit = Button(leftMenu,text="Calculator",image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_exit = Button(leftMenu,text="Purchase",image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_exit = Button(leftMenu,text="Supplier",image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)
        btn_exit = Button(leftMenu,command=self.logout,text="Exit",image=self.leftbtn_icon,compound=LEFT, padx=5, anchor='w',cursor="hand2",bd=3,font=("times new roman",15,"bold"), bg="White").pack(side=TOP,fill=X)


         #====== body content =======#
        self.label_product = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_product.place(x=300,y=120,height=150,width=300)

        self.label_expenses = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_expenses.place(x=650,y=120,height=150,width=300)

        self.label_cash = Label(self.root, text="Transactions\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_cash.place(x=1000,y=120,height=150,width=300)

        self.label_dealers = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_dealers.place(x=300,y=300,height=150,width=300)

        self.label_consumers = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_consumers .place(x=659,y=300,height=150,width=300)

        
        self.label_kg = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_kg.place(x=1000,y=300,height=150,width=300)

        #########################
        self.label_transfer = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_transfer.place(x=300,y=480,height=80,width=300)

        self.label_pos = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_pos .place(x=659,y=480,height=80,width=300)

        
        self.label_tsale = Label(self.root, text="",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.label_tsale.place(x=1000,y=480,height=80,width=300)



        #===== Footer  =======

        footer_label = Label(self.root, text="Inventory management system | Developed by Moxieus Technology\n for technical issue contact 07089184071",compound=LEFT,bg="#4d636d",fg="white", font=("times new roman",12)).pack(side=BOTTOM, fill=X)
        self.TotalProduct()

    def TotalProduct(self):

        ## number of Avaiable product
        self.my_conn.execute("select * from product_tb")
        rows = self.my_conn.fetchall()
        #self.label_product.config(text ="Total Product\n["+ str(self.my_conn.rowcount) +"]")


        ## ========= for total sale =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s",(self.today,))
        resul =self.my_conn.fetchall()
        for row in resul:
            self.totalsales.append(float(row[3]))
    
        self.label_product.config(text="Total Sales\n[#"+str(sum(self.totalsales)) +"]")
        self.conn.commit()

         ## ========= for total Expense =============== #

        self.my_conn.execute("select * from expenses_tb where dt=%s",(self.today,))
        resu =self.my_conn.fetchall()
        for ro in resu:
            #print(ro)
            self.totalexpenses.append(float(ro[2]))
    
        self.label_expenses.config(text="Total Expenses\n[#"+str(sum(self.totalexpenses)) +"]")
        self.conn.commit()

         ## ========= for total cash =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and paymentType=%s",(self.today,"Cash"))
        result =self.my_conn.fetchall()
        
        for ri in result:
            self.totalcash.append(float(ri[3]))
    
        self.label_cash.config(text="Total Cash\n[#"+str(sum(self.totalcash)) +"]")
        self.conn.commit()


        ## ========= for total invoice =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and product_name=%s",(self.today,"Gas"))
        re =self.my_conn.fetchall()
        
        for ni in re:
            self.totalKg.append(float(ni[2]))
    
        self.label_kg.config(text="Total kg Sold \n["+str(sum(self.totalKg)) +"kg]")
        self.conn.commit()

         ## ========= for total pos =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and paymentType=%s",(self.today,"Pos"))
        tel =self.my_conn.fetchall()
        
        for nl in tel:
            self.totalPos.append(float(nl[3]))
    
        self.label_pos.config(text="Total Pos  \n[#"+str(sum(self.totalPos)) +"]")
        self.conn.commit()

        ## ========= for total Transfer =============== #

        self.my_conn.execute("select * from transaction_tb where dt=%s and paymentType=%s",(self.today,"Transfer"))
        Fo =self.my_conn.fetchall()
        po = []
        for lo in Fo:
            po.append(float(lo[3]))
           
            self.totalTransfer.append(float(lo[3]))
            
        self.label_transfer.config(text="Total Transfer \n[#"+str(sum(self.totalTransfer)) +"]")
        self.conn.commit()

        ## ========= for total exavalut sell for the day =============== #
        tpsale = sum(self.totalcash)
        texp = sum(self.totalexpenses)
        unspend_cash = tpsale - texp
        self.label_tsale.config(text="Remaining Bal Exp \n[#"+str(unspend_cash) +"]")


        ## ========= for total present count =============== #

        self.my_conn.execute("select * from invoice_tb where dt=%s and remark=%s",(self.today,"Dealers"))
        reu = self.my_conn.fetchall()
    
        
    
        self.label_dealers.config(text="Present No of Dealers \n["+str(self.my_conn.rowcount)+"]")
        self.conn.commit()


         ## ========= for total constumer present count =============== #

        self.my_conn.execute("select * from invoice_tb where dt=%s and remark=%s",(self.today,"Consumers"))
        reu = self.my_conn.fetchall()
        
        
    
        self.label_consumers.config(text="Present No of Consumer \n["+str(self.my_conn.rowcount)+"]")
        self.conn.commit()
        



#================================= sidebar new windows ===================#

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

    def history(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = History(self.new_window)

    def invoice(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = Invoice(self.new_window)
    def logout(self):
        self.root.destroy()
        import login

root = Tk()
obj = Admin(root)
root.mainloop()