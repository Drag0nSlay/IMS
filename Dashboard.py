from tkinter import *
from tkinter import ttk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time
from datetime import datetime

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System  |  Developed By Aman Kothari")
        self.root.config(bg="white")

        # Title
        self.icon_title = PhotoImage(file="logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="orange", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout Button
        btn_logout = Button(self.root, text="Logout",command=self.logout,font=("times new roman", 20, "bold"), bg="yellow", cursor="hand2")
        btn_logout.place(x=1150, y=10, height=50, width=150)

        #====Clock====
        self.lbl_clock = Label(self.root, text="", font=("times new roman", 15), bg="green", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.tick()

        # Left Menu
        self.menu_logo = PhotoImage(file="menuLogo.png")
        LeftMenu= Frame(self.root, bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=20,y=102,width=210,height=565)

        lbl_menulogo= Label(LeftMenu,image=self.menu_logo)
        lbl_menulogo.pack(side=TOP,fill=X)

        self.icon_side = PhotoImage(file="side.png").subsample(15)

        lbl_menulogo=Label(LeftMenu,text="Menu",font=("times new roman",15),bg="#009688")
        lbl_menulogo.pack(side=TOP,fill=X)
        
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        btn_employee.pack(side=TOP,fill=X)
        
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        btn_supplier.pack(side=TOP,fill=X)
        
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        btn_category.pack(side=TOP,fill=X)
        
        btn_product=Button(LeftMenu,text="product",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        btn_product.pack(side=TOP,fill=X)
        
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        btn_sales.pack(side=TOP,fill=X)
        
        btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        btn_exit.pack(side=TOP,fill=X)

        # Content
        self.lbl_employee = Label(self.root, text="Total Employee\n[ 3 ]",bd=5,relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, width=300, height=150)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[ 3 ]",bd=5,relief=RIDGE, bg="#ff5722", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, width=300, height=150)

        self.lbl_category = Label(self.root, text="Total Category\n[ 3 ]",bd=5,relief=RIDGE, bg="#009688", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, width=300, height=150)

        self.lbl_product = Label(self.root, text="Total Product\n[ 3 ]",bd=5,relief=RIDGE, bg="#607d8b", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, width=300, height=150)

        self.lbl_sales = Label(self.root, text="Total Sales\n[ 3 ]",bd=5,relief=RIDGE, bg="#ffc107", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, width=300, height=150)



        # Footer
        lbl_Footer = Label(self.root, text="IMS-Inventory Management System\n For any Technical Issue Contact: CodeCrusaders", font=("times new roman", 12), bg="green", fg="white")
        lbl_Footer.place(x=0, y=750, relwidth=1, height=50)   

        self.update_content()

    def tick(self):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {date_time}")
        self.lbl_clock.after(1000, self.tick)
#------------------------------------------------------------------------------------------------------

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)


    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Product\n[ {str(len(product))} ]')
        
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')
        
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Category\n[ {str(len(category))} ]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))} ]')
        
            self.lbl_sales.config(text=f'Total Sales\n[{str(len(os.listdir('bill')))}]')

            #time_=time.strftime("%I:%M:%S")
            #date_=time.strftime("%d-%m-%Y")
            #self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            #self.lbl_clock.after(200,self.update_content)


        except Exception as ex:
          messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def logout(self):
        try:
            self.root.destroy()
            os.system("python login.py")
 
        except FileNotFoundError:
            messagebox.showerror("Error", "login.py file not found.", parent=self.root)

if __name__=="__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
