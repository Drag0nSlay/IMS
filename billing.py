from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime
import time
import os
import tempfile
from tkinter import messagebox

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System  |  Developed By Aman Kothari")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0

        # Title
        self.icon_title = PhotoImage(file="logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="orange", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout Button
        btn_logout = Button(self.root, text="Logout",command=self.logout,font=("times new roman", 20, "bold"), bg="yellow", cursor="hand2")
        btn_logout.place(x=1150, y=10, height=50, width=150)

        #====Clock====
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="green", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.tick()

        #====Product Frame====
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE)
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        ptitle= Label(ProductFrame1,text="All Products",font=("goudy old style",20),bg="#262626",fg="white").pack(side=TOP,fill=X)

#===============Product Search Frame===========
        self.var_search=StringVar()
        
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search= Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_search= Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search= Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        btn_search= Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=280,y=45,width=100,height=25)
        btn_show_all= Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=280,y=10,width=100,height=25)
   
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set,show="headings")

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
      
        self.productTable.heading("pid",text="PID")
        self.productTable.heading("name",text="Name")
        self.productTable.heading("price",text="Price")
        self.productTable.heading("qty",text="Quantity")
        self.productTable.heading("status",text="Status")

        self.productTable["show"]="headings"

        self.productTable.column("pid",width=40)
        self.productTable.column("name",width=100)
        self.productTable.column("price",width=100)
        self.productTable.column("qty",width=40)
        self.productTable.column("status",width=90)
        self.productTable.pack(fill=BOTH,expand=1)

        self.productTable.bind("<ButtonRelease-1>",self.get_data)
        lbl_note= Label(ProductFrame1,text="Note: 'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",13),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

#========Customer Frame========
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE)
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        ctitle= Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)

        lbl_name= Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name= Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)

        lbl_contact= Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
        txt_contact= Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)

        #===Cal Cart Frame===#
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE)
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        #===Calculator Frame===#
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        self.txt_cal_input= Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        self.txt_cal_input.grid(row=0,columnspan=4)

        btn_7= Button(Cal_Frame,text='7',font=('arial',15,'bold',),command=lambda:self.get_input(7),cursor="hand2",bd=5,width=4,pady=10).grid(row=1,column=0)
        btn_8= Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),cursor="hand2",bd=5,width=4,pady=10).grid(row=1,column=1)
        btn_9= Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),cursor="hand2",bd=5,width=4,pady=10).grid(row=1,column=2)
        btn_sum= Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),cursor="hand2",bd=5,width=4,pady=10).grid(row=1,column=3)

        btn_4= Button(Cal_Frame,text='4',font=('arial',15,'bold',),command=lambda:self.get_input(4),cursor="hand2",bd=5,width=4,pady=10).grid(row=2,column=0)
        btn_5= Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),cursor="hand2",bd=5,width=4,pady=10).grid(row=2,column=1)
        btn_6= Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),cursor="hand2",bd=5,width=4,pady=10).grid(row=2,column=2)
        btn_sub= Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),cursor="hand2",bd=5,width=4,pady=10).grid(row=2,column=3)

        btn_1= Button(Cal_Frame,text='1',font=('arial',15,'bold',),command=lambda:self.get_input(1),cursor="hand2",bd=5,width=4,pady=10).grid(row=3,column=0)
        btn_2= Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),cursor="hand2",bd=5,width=4,pady=10).grid(row=3,column=1)
        btn_3= Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),cursor="hand2",bd=5,width=4,pady=10).grid(row=3,column=2)
        btn_mul= Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),cursor="hand2",bd=5,width=4,pady=10).grid(row=3,column=3)

        btn_0= Button(Cal_Frame,text='0',font=('arial',15,'bold',),command=lambda:self.get_input(0),cursor="hand2",bd=5,width=4,pady=15).grid(row=4,column=0)
        btn_c= Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,cursor="hand2",bd=5,width=4,pady=15).grid(row=4,column=1)
        btn_eq= Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,cursor="hand2",bd=5,width=4,pady=15).grid(row=4,column=2)
        btn_div= Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),cursor="hand2",bd=5,width=4,pady=15).grid(row=4,column=3)


        #===Cart Frame===#
        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle= Label(Cart_Frame,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set,show="headings")

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
      
        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="QTY.")

        self.CartTable["show"]="headings"

        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)

        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #====ADD CART Widgets Frame====
        self.var_pid= StringVar()
        self.var_pname= StringVar()
        self.var_price= StringVar()
        self.var_qty= StringVar()
        self.var_stock  = StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name= Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name= Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price= Label(Add_CartWidgetsFrame,text="Price per Qty.",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price= Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        
        lbl_p_qty= Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty= Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)
    
        self.lbl_inStock= Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)
    

#==============Billing Area==================
        BillFrame= Frame(self.root,bd=2,relief=RIDGE,bg='white')
        BillFrame.place(x=953,y=110,width=410,height=410)

        Btitle= Label(BillFrame,text="Customer Bill Area",font=("goudy old style",20),bg="red",fg="white").pack(side=TOP,fill=X)
        scrolly= Scrollbar(BillFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area= Text(BillFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

#=============Biling Area=================
        BillMenuFrame= Frame(self.root,bd=2,relief=RIDGE,bg='white')
        BillMenuFrame.place(x=953,y=520,width=410,height=140)
        
        self.lbl_amnt= Label(BillMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount= Label(BillMenuFrame,text="Discount\n[%5]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay= Label(BillMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        btn_print= Button(BillMenuFrame,text="Print",command=self.print_bill,cursor='hand2',font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all= Button(BillMenuFrame,text="Clear All",command=self.clear_all,cursor='hand2',font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(BillMenuFrame,text="Generate/Save Bill",command=self.generate_bill,cursor='hand2',font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=50)

#================Footer=======================
        Footer = Label(self.root, text="IMS-Inventory Management System\n For any Technical Issue Contact: CodeCrusaders", font=("times new roman", 12), bg="Darkblue", fg="white")
        Footer.place(x=0, y=750, relwidth=1, height=50)   

        Footer2 = Label(self.root, text="Read the Documentation Below \nhttps://api.hive.blog/v1/database/get_dynamic_global_properties ",cursor='hand2',font=("times new roman", 12), bg="Crimson", fg="white")
        Footer2.place(x=0, y=660, relwidth=1, height=40)   

        self.show()
        #self.bill_top()
        #self.update_date_time()
#===================All Functions====================
    def get_input(self,num):
        xnum= self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')
    
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status= 'Active'")
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children(  ))
            for row in rows:
                self.productTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root )

    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status= 'Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(*self.productTable.get_children(  ))
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
    

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)
        elif self.var_qty.get()=='': 
            messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()): 
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        
        else:
            #price_cal= int(self.var_qty.get())+float(self.var_price.get())
            #price_cal= float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #self.cart_list.append(cart_data)

#update cart============================
            present='no'
            index_=0 
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update | Remove from the cart list",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_qty.get() #qty
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amnt.\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")



    def show_cart(self):
        try:
            
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent= self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the cart",parent= self.root)
        else:
            #=====Bill Top=====
            self.bill_top()
            #=====Bill Middle=====
            self.bill_middle()
            #=====Bill Bottom=====
            self.bill_bottom() 

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Save in Backend",parent=self.root)
            self.chk_print=1

    def bill_top(self):
        self.invoice=time.strftime("%H%M%S")+time.strftime("%d%m%Y")
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 98765***** , Delhi=125001
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQty\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''

        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:      
            for row in self.cart_list:
                
                pid=row[0]
                name=row[1]
                qty= int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #=========update qty in product table=========
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.clear_cart()
        self.show()
        self.show_cart()
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.chk_print=0

    #def update_date_time(self):
      #  time_=time.strftime("%I:%M:%S")
       # date_=time.strftime("%d-%m-%Y")
        #self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        #self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill, to print the receipt",parent=self.root)
            
    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def tick(self):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {date_time}")
        self.lbl_clock.after(1000, self.tick)
    


if __name__=="__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()