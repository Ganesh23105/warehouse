from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk

def clear():
    product_id_entry.delete(0, END)
    product_name_entry.delete(0, END)
    location_entry.delete(0,END)
    quantity_entry.delete(0, END)

def products_addition():
    if product_id_entry.get()=='' or product_name_entry.get()=='' or location_entry.get()=='' or quantity_entry.get()=='':
        messagebox.showerror('Error','All Fields should be filled.')
    else:
        try:
            con = pymysql.connect(host='localhost',user='root',password='root')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again.')
            return
        
        query='use warehouse'
        mycursor.execute(query)
        try:
            query = 'create table products(product_id VARCHAR(255) NOT NULL PRIMARY KEY,product_name VARCHAR(255) NOT NULL,location VARCHAR(50) NOT NULL,quantity VARCHAR(255) NOT NULL)'
            mycursor.execute(query)
        except:
            pass
        query = 'select * from products where product_id=%s'
        mycursor.execute(query,(product_id_entry.get()))
        row = mycursor.fetchone()

        if row != None:
            query = "select product_name from products where product_id=%s"
            mycursor.execute(query,product_id_entry.get())  
            value = mycursor.fetchone()        
            messagebox.showerror('Error','Product ID Already Exists as '+str(value[0]))
        else:
            query = 'insert into products(product_id, product_name, location, quantity) values(%s,%s,%s,%s)'
            mycursor.execute(query,(product_id_entry.get(),product_name_entry.get(),location_entry.get(),quantity_entry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success','Product added')
            clear()
            quantity_entry.bind('<Return>',product_id_entry.focus())

def order_update():
    hide_frame(add_frame)
    hide_frame(add_order_frame)
    hide_frame(retrive_frame)
    show_frame(order_update_frame)

def order_add():
    hide_frame(order_update_frame)
    hide_frame(add_frame)
    hide_frame(retrive_frame)
    show_frame(add_order_frame)

def retrive_product():
    hide_frame(order_update_frame)
    hide_frame(add_frame)
    hide_frame(add_order_frame)
    show_frame(retrive_frame)
    
def add_product():
    hide_frame(order_update_frame)
    hide_frame(retrive_frame)
    hide_frame(add_order_frame)
    add_frame.place(relx=0.5,rely=0.5,anchor='center')

def show_frame(frame):
    frame.place(relx=0.5,rely=0.5,anchor='center')

def hide_frame(frame):
    frame.place_forget()

root = Tk()
root.title("Home")
root.geometry("1200x675")

left_frame = Frame(root,bg = "lightgray")
left_frame.place(relx=0,rely=0,relwidth=0.25,relheight=1)

left_frame.columnconfigure(0,weight=1)
left_frame.rowconfigure((0,1,2,3),weight=1,uniform='a')

#product Lframe
product_Lframe = LabelFrame(left_frame, text="Products",font=("Poppins",12,"bold"))
product_Lframe.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

product_add_button=Button(product_Lframe,text="ADD",command=add_product,bd=0,font=("Times New Roman",15,"bold"),bg="#163246",fg="white")
product_add_button.pack(expand=True,padx=50,pady=(10,15),fill='both')

product_retrive_button=Button(product_Lframe,command=retrive_product,text="SEARCH",bd=0,font=("Times New Roman",15,"bold"),bg="#163246",fg="white")
product_retrive_button.pack(expand=True,padx=50,pady=(0,15),fill='both')

#order Lframe
order_Lframe = LabelFrame(left_frame,text="Orders",font=("Poppins",13,"bold"))
order_Lframe.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")

order_update_button=Button(order_Lframe,text="UPDATE",command=order_update,bd=0,font=("Times New Roman",15,"bold"),bg="#163246",fg="white")
order_update_button.pack(expand=True,padx=50,pady=(10,15),fill='both')

order_add_button=Button(order_Lframe,text="ADD",command=order_add,bd=0,font=("Times New Roman",15,"bold"),bg="#163246",fg="white")
order_add_button.pack(expand=True,padx=50,pady=(0,15),fill='both')

right_frame=Frame(root)
right_frame.place(relx=0.25,rely=0,relwidth=0.75,relheight=1)

# add button in products

add_frame = Frame(right_frame)

product_id_label=Label(add_frame,text="PRODUCT ID",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
product_id_label.grid(row=0,column=0,padx=10,pady=10,sticky="e")
product_id_entry=Entry(add_frame,bd=4,relief=GROOVE)
product_id_entry.grid(row=0,column=1,padx=10,pady=10)

product_name_label=Label(add_frame,text="PRODUCT NAME",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
product_name_label.grid(row=1,column=0,padx=10,pady=10,sticky="e")
product_name_entry=Entry(add_frame,bd=4,relief=GROOVE)
product_name_entry.grid(row=1,column=1,padx=10,pady=10)

location_label=Label(add_frame,text="LOCATION",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
location_label.grid(row=2,column=0,padx=10,pady=10,sticky="e")
location_entry=Entry(add_frame,bd=4,relief=GROOVE)
location_entry.grid(row=2,column=1,padx=10,pady=10)

quantity_label=Label(add_frame,text="QUANTITY",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
quantity_label.grid(row=3,column=0,padx=10,pady=10,sticky="e")
quantity_entry=Entry(add_frame,bd=4,relief=GROOVE)
quantity_entry.grid(row=3,column=1,padx=10,pady=10)

submit_button=Button(add_frame,text="SUBMIT",bd=0,font=("Times New Roman",15,"bold"),bg="#163246",fg="white",width=13,command=products_addition)
submit_button.grid(row=4,column=0,columnspan=2)

product_id_entry.bind('<Return>',lambda event :product_name_entry.focus())
product_name_entry.bind('<Return>',lambda event :location_entry.focus())
location_entry.bind('<Return>',lambda event :quantity_entry.focus())

#retrieve product 
retrive_frame=Frame(right_frame)

combo_var_stream=StringVar()
combo_box_stream =ttk.Combobox(retrive_frame,textvariable=combo_var_stream,state="readonly")
combo_box_stream['values'] = ('Product ID', 'Product Name', 'Location')
combo_box_stream.grid(row=0,column=0)
combo_box_stream.set("Select")

def show_table():

    if combo_box_stream.get()=='Select' or entryfield_entry.get()=='':
        messagebox.showerror('Error','All Fields should be filled.')
    else:
        try:
            con = pymysql.connect(host='localhost',user='root',password='root')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again.')
            return
        
        query='use warehouse'
        mycursor.execute(query)

        def add_data(tree, product_id, product_name, location, quantity):
            tree.insert("", "end", values=(product_id, product_name, location, quantity))
        
        def on_select(event):
            selected_item = tree.selection()[0]  # Get the selected item (row)
            values = tree.item(selected_item, 'values')  # Get the values of the selected row

        def change_selected_row():
            selected_item = tree.selection()[0]
            # print(selected_item)
            values = tree.item(selected_item, 'values')
            # print(values)


            def products_updation():
                try:
                    con = pymysql.connect(host='localhost',user='root',password='root')
                    mycursor = con.cursor()
                except:
                    messagebox.showerror('Error','Connection is not established try again.')
                    return
        
                query='use warehouse'
                mycursor.execute(query)
                
                query="UPDATE products SET product_name = %s, location = %s, quantity = %s WHERE product_id = %s"
                # print(product_id_entry)
                mycursor.execute(query,(product_name_entry.get(),location_entry.get(),quantity_entry.get(),product_id_entry.get()))
                con.commit()
                messagebox.showinfo('Success','Product Successfully Updated.')
                window.destroy()


            window = Toplevel()
            window.title("Change Products")

            product_id_label=Label(window,text="PRODUCT ID")
            product_id_label.grid(row=0,column=0)
            product_id_entry=Entry(window)
            product_id_entry.grid(row=0,column=1)
            product_id_entry.insert(0,values[0])
            product_id_entry.config(state=DISABLED)

            product_name_label=Label(window,text="PRODUCT NAME")
            product_name_label.grid(row=1,column=0)
            product_name_entry=Entry(window)
            product_name_entry.grid(row=1,column=1)
            product_name_entry.insert(0,values[1])

            location_label=Label(window,text="LOCATION")
            location_label.grid(row=2,column=0)
            location_entry=Entry(window)
            location_entry.grid(row=2,column=1)
            location_entry.insert(0,values[2])

            quantity_label=Label(window,text="QUANTITIY")
            quantity_label.grid(row=3,column=0)
            quantity_entry=Entry(window)
            quantity_entry.grid(row=3,column=1)
            quantity_entry.insert(0,values[3])

            submit_button=Button(window,text="SUBMIT",command=products_updation)
            submit_button.grid(row=4,column=0,columnspan=2)

        table_frame = Frame(retrive_frame)
        table_frame.grid(row=1, column=0,columnspan=3)

        change_button = Button(retrive_frame, text="Change Selected Row", command=change_selected_row)
        change_button.grid(row=2, column=0,columnspan=3)

        tree = ttk.Treeview(table_frame, columns=("Product ID", "Product Name", "Location","Quantity"), show="headings")

        tree.heading("Product ID", text="Product ID")
        tree.heading("Product Name", text="Product Name")
        tree.heading("Location", text="Location")
        tree.heading("Quantity", text="Quantity")
                
        # add_data(tree, "John Doe", "25", "USA","ui")
        if combo_box_stream.get()=='Product ID':
            query='select * from products where product_id=%s'
            mycursor.execute(query,entryfield_entry.get())
            row = mycursor.fetchall()
            if row==None:
                messagebox.showerror('Error','Filled credantials does not present')
            else:
                for i in row:
                    add_data(tree,i[0],i[1],i[2],i[3])
        elif combo_box_stream.get()=="Product Name":
            query='select * from products where product_name=%s'
            mycursor.execute(query,entryfield_entry.get())
            row = mycursor.fetchall()
            if row==None:
                messagebox.showerror('Error','Filled credantials does not present')
            else:
                for i in row:
                    add_data(tree,i[0],i[1],i[2],i[3])
        elif combo_box_stream.get()=="Location":
            query='select * from products where Location=%s'
            mycursor.execute(query,entryfield_entry.get())
            row = mycursor.fetchall()
            if row==None:
                messagebox.showerror('Error','Filled credantials does not present')
            else:
                for i in row:
                    add_data(tree,i[0],i[1],i[2],i[3])

        
            
        tree.pack(side="left", fill="both", expand=True)

show_button=Button(retrive_frame,text="SHOW",command=show_table)
show_button.grid(row=0,column=2)
        
entryfield_entry=Entry(retrive_frame)
entryfield_entry.grid(row=0,column=1)
# bgfImage= ImageTk.PhotoImage(file='image\\4.2.jpg')
empty_frame = Frame(right_frame)

# image_label=Label(empty_frame,image=bgfImage)
# image_label.pack(side=RIGHT,fill=BOTH,expand=True)

# add order

def show1_table():

    def add_data(tree, product_id, product_name, location, quantity):
        tree.insert("", "end", values=(product_id, product_name, location, quantity))

    table_frame = Frame(add_order_frame)
    table_frame.grid(row=4, column=0,columnspan=3)

    tree = ttk.Treeview(table_frame, columns=("Product ID", "Product Name", "Location", "Quantity"), show="headings")

    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Location", text="Location")
    tree.heading("Quantity", text="Quantiy")
            
    add_data(tree, "John Doe", "25", "USA","ui")

    y_scrollbar = ttk.Scrollbar(add_order_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)
        
    tree.pack(side="left", fill="both", expand=True)
    y_scrollbar.pack(side="right", fill="y")

add_order_frame = Frame(right_frame)

order_id_label=Label(add_order_frame,text="Order ID")
order_id_label.grid(row=0,column=0)
order_id_entry=Entry(add_order_frame)
order_id_entry.grid(row=0,column=1)

source_label=Label(add_order_frame,text="Source")
source_label.grid(row=1,column=0)
source_entry=Entry(add_order_frame)
source_entry.grid(row=1,column=1)

destination_label=Label(add_order_frame,text="Destination")
destination_label.grid(row=2,column=0)
destination_entry=Entry(add_order_frame)
destination_entry.grid(row=2,column=1)

products_in_order_label = Label(add_order_frame,text="Products")
products_in_order_label.grid(row=3,column=0)
products_in_order_entry=Entry(add_order_frame)
products_in_order_entry.grid(row=3,column=1)
ok_button = Button(add_order_frame,text="Show",command=show1_table)
ok_button.grid(row=3,column=2)

#update status of order

def show2_table():

    def add_data(tree, product_id, product_name, location, quantity):
        tree.insert("", "end", values=(product_id, product_name, location, quantity))

    table_frame = Frame(order_update_frame)
    table_frame.grid(row=2, column=0,columnspan=2)

    tree = ttk.Treeview(table_frame, columns=("Product ID", "Product Name", "Location", "Quantity"), show="headings")

    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Location", text="Location")
    tree.heading("Quantity", text="Quantiy")
            
    add_data(tree, "John Doe", "25", "USA","ui")

    y_scrollbar = ttk.Scrollbar(order_update_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)
        
    tree.pack(side="left", fill="both", expand=True)
    y_scrollbar.pack(side="right", fill="y")

order_update_frame = Frame(right_frame)

order_id_label=Label(order_update_frame,text="Order ID")
order_id_label.grid(row=0,column=0)
order_id_entry=Entry(order_update_frame)
order_id_entry.grid(row=0,column=1)

products_in_order_label = Label(order_update_frame,text="Products")
products_in_order_label.grid(row=1,column=0)
ok_button = Button(order_update_frame,text="Show",command=show2_table)
ok_button.grid(row=1,column=1)

show_frame(empty_frame)

root.mainloop()