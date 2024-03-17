from tkinter import *
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk

def clear():
    product_id_entry.delete(0, END)
    product_name_entry.delete(0, END)
    location_entry.delete(0,END)
    quantity_entry.delete(0, END)

def database_add_products():
    if product_id_entry.get()=='' or product_name_entry.get()=='' or location_entry.get()=='' or quantity_entry.get()=='' or brand_combobox.get()=='SELECT' or category_combobox.get()=='SELECT' or (brand_combobox.get()=='NEW' and product_brand_entry.get()=='') or (category_combobox.get()=='NEW' and product_category_entry.get()==''):
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
            query = 'create table products(product_id VARCHAR(255) NOT NULL PRIMARY KEY,product_name VARCHAR(255) NOT NULL,brand VARCHAR(50),category VARCHAR(50), location VARCHAR(50) NOT NULL,quantity VARCHAR(255) NOT NULL)'
            mycursor.execute(query)
        except:
            pass
        query = 'select * from products where product_id=%s'
        mycursor.execute(query,(product_id_entry.get()))
        row = mycursor.fetchone()

        if brand_combobox.get() == "NEW":
            brand = product_brand_entry.get()
        else:
            brand = brand_combobox.get()

        if category_combobox.get() == "NEW":
            category = product_category_entry.get()
        else:
            category = category_combobox.get()

        if row != None:
            query = "select product_name from products where product_id=%s"
            mycursor.execute(query,product_id_entry.get())  
            value = mycursor.fetchone()        
            messagebox.showerror('Error','Product ID Already Exists as '+str(value[0]))
        else:
            query = 'insert into products(product_id, product_name, brand, category, location, quantity) values(%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(product_id_entry.get(),product_name_entry.get(),brand,category,location_entry.get(),quantity_entry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success','Product added')
            clear()
            quantity_entry.bind('<Return>',product_id_entry.focus())

def order_view():
    add_frame.place_forget()
    add_order_frame.place_forget()
    view_product_frame.place_forget()
    order_view_frame.place(relx=0.025,rely=0.05,relwidth=0.95,relheight=0.9)

def order_add():
    order_view_frame.place_forget()
    add_frame.place_forget()
    view_product_frame.place_forget()
    add_order_frame.place(relx=0.025,rely=0.05,relwidth=0.95,relheight=0.9)

def view_product():
    order_view_frame.place_forget()
    add_frame.place_forget()
    add_order_frame.place_forget()
    view_product_frame.place(relx=0.025,rely=0.05,relwidth=0.95,relheight=0.9)
    retrieve_product_data()
    
def add_product():
    order_view_frame.place_forget()
    view_product_frame.place_forget()
    add_order_frame.place_forget()
    add_frame.place(relx=0.025,rely=0.05,relwidth=0.95,relheight=0.9)

def show_frame(frame):
    frame.place(relx=0.5,rely=0.5,anchor='center')

def enable_entry(event):
    if brand_combobox.get() == "NEW":
        product_brand_entry.configure(state="normal")
    else:
        product_brand_entry.delete(0,END)
        product_brand_entry.configure(state="readonly")
    if category_combobox.get() == "NEW":
        product_category_entry.configure(state="normal")
    else:
        product_category_entry.delete(0,END)
        product_category_entry.configure(state="readonly")       

def flatten_tuple(nested_tuple):
    flattened = []
    for item in nested_tuple:
        if isinstance(item, tuple):
            flattened.extend(flatten_tuple(item))
        else:
            flattened.append(item)
    return flattened

def combo_group_by():
    try:
        con = pymysql.connect(host='localhost',user='root',password='root', database='warehouse')
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error','Connection is not established try again.')
        return
    brand_query = 'SELECT brand FROM products GROUP BY brand ORDER BY brand ASC'
    category_query = 'SELECT category FROM products GROUP BY category ORDER BY category ASC'
    mycursor.execute(brand_query)
    brand_ntup = mycursor.fetchall()
    mycursor.execute(category_query)
    category_ntup = mycursor.fetchall()
    # print(brand_values, category_values)
    return brand_ntup, category_ntup

def retrieve_product_data():
    # Iterate over all items in the treeview and delete them
    for item in view_product_tree.get_children():
        view_product_tree.delete(item)
    try:
        con = pymysql.connect(host='localhost',user='root',password='root')
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error','Database Connectivity Issue, Try Again')
        return 
    
    query='use warehouse'
    mycursor.execute(query)

    all_data = "select * from products"
    mycursor.execute(all_data)
    fetch_all = mycursor.fetchall()
    for i in fetch_all:
        view_product_tree.insert("", "end", values=(i[0], i[1], i[4], i[5],i[2],i[3]))

    data = [(view_product_tree.set(child, 1),view_product_tree.set(child, 0), child) for child in view_product_tree.get_children('')]
    data.sort(key=lambda x: (x[0], x[1]))
    for index, (name,id, child) in enumerate(data):
        view_product_tree.move(child, '', index)

def change_selected_row():
    selected_item = view_product_tree.selection()[0]
    # print(selected_item)
    values = view_product_tree.item(selected_item, 'values')
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

    quantity_label=Label(window,text="QUANTITY")
    quantity_label.grid(row=3,column=0)
    quantity_entry=Entry(window)
    quantity_entry.grid(row=3,column=1)
    quantity_entry.insert(0,values[3])

    update_button=Button(window,text="UPDATE",command=products_updation)
    update_button.grid(row=4,column=0,columnspan=2)

def search_product():
    for item in view_product_tree.get_children():
        view_product_tree.delete(item)

    if select_type_combobox.get()=='Select' or select_type_entry.get()=='':
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

                
        if select_type_combobox.get()=='Product ID':
            query='select * from products where product_id=%s'
            mycursor.execute(query,select_type_entry.get())
            row = mycursor.fetchall()
            if row==None:
                messagebox.showerror('Error','Filled credantials does not present')
            else:
                for i in row:
                    view_product_tree.insert("", "end", values=(i[0], i[1], i[4], i[5],i[2],i[3]))
        elif select_type_combobox.get()=="Product Name":
            query='select * from products where product_name=%s'
            mycursor.execute(query,select_type_entry.get())
            row = mycursor.fetchall()
            if row==None:
                messagebox.showerror('Error','Filled credantials does not present')
            else:
                for i in row:
                    view_product_tree.insert("", "end", values=(i[0], i[1], i[4], i[5],i[2],i[3]))
        elif select_type_combobox.get()=="Location":
            query='select * from products where Location=%s'
            mycursor.execute(query,select_type_entry.get())
            row = mycursor.fetchall()
            if row==None:
                messagebox.showerror('Error','Filled credantials does not present')
            else:
                for i in row:
                    view_product_tree.insert("", "end", values=(i[0], i[1], i[4], i[5],i[2],i[3]))

root = Tk()
root.title("employee page")
root.geometry("1200x675")
root.resizable(0,0)

left_frame = Frame(root,bg ="#E9E3D5")
left_frame.place(relx=0,rely=0,relwidth=0.2,relheight=1)

left_frame.columnconfigure(0,weight=1)

#product Lframe
product_Lframe = LabelFrame(left_frame, text="Products")
product_Lframe.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")
product_Lframe.columnconfigure(0,weight=1)

product_add_button=Button(product_Lframe,text="ADD",command=add_product)
product_add_button.grid(row=0,column=0)

product_view_button=Button(product_Lframe,text="VIEW",command=view_product)
product_view_button.grid(row=1,column=0)

#order Lframe
order_Lframe = LabelFrame(left_frame,text="Orders")
order_Lframe.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")
order_Lframe.columnconfigure(0,weight=1)

order_add_button=Button(order_Lframe,text="ADD",command=order_add)
order_add_button.grid(row=0,column=0)

order_view_button=Button(order_Lframe,text="VIEW",command=order_view)
order_view_button.grid(row=1,column=0)

right_frame=Frame(root,bg ="#E9E3D5")
right_frame.place(relx=0.2,rely=0,relwidth=0.8,relheight=1)

# add button in products

add_frame = Frame(right_frame,borderwidth=5,relief='groove',bg="white")

product_id_label=Label(add_frame,text="PRODUCT ID")
product_id_label.grid(row=0,column=0)
product_id_entry=Entry(add_frame)
product_id_entry.grid(row=0,column=1)

product_name_label=Label(add_frame,text="PRODUCT NAME")
product_name_label.grid(row=1,column=0)
product_name_entry=Entry(add_frame)
product_name_entry.grid(row=1,column=1)

brand_nt, category_nt = combo_group_by()
brand_values = flatten_tuple(brand_nt)
category_values = flatten_tuple(category_nt)
brand_values.append('NEW')
category_values.append('NEW')

product_brand_label=Label(add_frame,text="BRAND")
product_brand_label.grid(row=2,column=0)
brand_combobox_var=StringVar()
brand_combobox =ttk.Combobox(add_frame,textvariable=brand_combobox_var,state="readonly")
brand_combobox['values'] = brand_values
brand_combobox.grid(row=2,column=1)
brand_combobox.set("SELECT")
brand_combobox.bind("<<ComboboxSelected>>", enable_entry)
product_brand_entry=Entry(add_frame, state='readonly')
product_brand_entry.grid(row=2,column=2)

product_category_label=Label(add_frame,text="CATEGORY")
product_category_label.grid(row=3,column=0)
category_combobox_var=StringVar()
category_combobox =ttk.Combobox(add_frame,textvariable=category_combobox_var,state="readonly")
category_combobox['values'] = category_values
category_combobox.grid(row=3,column=1)
category_combobox.set("SELECT")
category_combobox.bind("<<ComboboxSelected>>", enable_entry)
product_category_entry=Entry(add_frame, state='readonly')
product_category_entry.grid(row=3,column=2)

location_label=Label(add_frame,text="LOCATION")
location_label.grid(row=4,column=0)
location_entry=Entry(add_frame)
location_entry.grid(row=4,column=1)

quantity_label=Label(add_frame,text="QUANTITY")
quantity_label.grid(row=5,column=0)
quantity_entry=Entry(add_frame)
quantity_entry.grid(row=5,column=1)

submit_button=Button(add_frame,text="SUBMIT",command=database_add_products)
submit_button.grid(row=6,column=0,columnspan=2)

#retrieve product 
view_product_frame=Frame(right_frame)

view_product_attributes_frame = Frame(view_product_frame,bg="white")
view_product_attributes_frame.place(relx=0,rely=0,relwidth=1,relheight=0.15)
view_product_attributes_frame.rowconfigure(0,weight=1)
view_product_attributes_frame.columnconfigure((0,1,2,3,4,5),weight=1)

select_type_combobox_var=StringVar()
select_type_combobox =ttk.Combobox(view_product_attributes_frame,textvariable=select_type_combobox_var,state="readonly")
select_type_combobox['values'] = ('Product ID', 'Product Name', 'Location')
select_type_combobox.grid(row=0,column=0)
select_type_combobox.set("SELECT")

select_type_entry=Entry(view_product_attributes_frame)
select_type_entry.grid(row=0,column=1) 

brand_label=Label(view_product_attributes_frame,text="BRAND")
brand_label.grid(row=0,column=2)
view_brand_combobox_var=StringVar()
view_brand_combobox =ttk.Combobox(view_product_attributes_frame,textvariable=view_brand_combobox_var,state="readonly")
view_brand_combobox['values'] = flatten_tuple(brand_nt)
view_brand_combobox.grid(row=0,column=3)
view_brand_combobox.set("SELECT")

category_label=Label(view_product_attributes_frame,text="CATEGORY")
category_label.grid(row=0,column=4)
view_category_combobox_var=StringVar()
view_category_combobox =ttk.Combobox(view_product_attributes_frame,textvariable=view_category_combobox_var,state="readonly")
view_category_combobox['values'] = flatten_tuple(category_nt)
view_category_combobox.grid(row=0,column=5)
view_category_combobox.set("SELECT")

table_frame = Frame(view_product_frame)
table_frame.place(relx=0,rely=0.15,relwidth=1,relheight=0.7)

view_product_tree = ttk.Treeview(table_frame, columns=("Product ID", "Product Name", "Location","Quantity","Brand","Category"), show="headings",height=100)

view_product_tree.heading("Product ID", text="Product ID")
view_product_tree.heading("Product Name", text="Product Name")
view_product_tree.heading("Location", text="Location")
view_product_tree.heading("Quantity", text="Quantity")
view_product_tree.heading("Category",text="Category")
view_product_tree.heading("Brand",text="Brand")

view_product_tree_y_scroll = Scrollbar(table_frame, orient="vertical", command=view_product_tree.yview)
view_product_tree.configure(yscrollcommand=view_product_tree_y_scroll.set)
view_product_tree_y_scroll.pack(side='right',fill=Y)

view_product_tree_x_scroll = Scrollbar(table_frame, orient="horizontal", command=view_product_tree.xview)
view_product_tree.configure(xscrollcommand=view_product_tree_x_scroll.set)
view_product_tree_x_scroll.pack(side='bottom',fill=X)

view_product_tree.pack()
        
view_product_button_frame = Frame(view_product_frame,bg="white")
view_product_button_frame.place(relx=0,rely=0.85,relheight=0.15,relwidth=1)
view_product_button_frame.rowconfigure(0,weight=1)
view_product_button_frame.columnconfigure((0,1,2),weight=1)

product_reset_button=CTkButton(view_product_button_frame,text="RESET",command=retrieve_product_data,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_reset_button.grid(row=0,column=0)

product_search_button=CTkButton(view_product_button_frame,text="SEARCH",command=search_product,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_search_button.grid(row=0,column=1)

product_view_button=CTkButton(view_product_button_frame,text="VIEW",command=change_selected_row,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_view_button.grid(row=0,column=2)


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

    table_frame = Frame(order_view_frame)
    table_frame.grid(row=2, column=0,columnspan=2)

    tree = ttk.Treeview(table_frame, columns=("Product ID", "Product Name", "Location", "Quantity"), show="headings")

    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Location", text="Location")
    tree.heading("Quantity", text="Quantiy")
            
    add_data(tree, "John Doe", "25", "USA","ui")

    y_scrollbar = ttk.Scrollbar(order_view_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)
        
    tree.pack(side="left", fill="both", expand=True)
    y_scrollbar.pack(side="right", fill="y")

order_view_frame = Frame(right_frame)

order_id_label=Label(order_view_frame,text="Order ID")
order_id_label.grid(row=0,column=0)
order_id_entry=Entry(order_view_frame)
order_id_entry.grid(row=0,column=1)

products_in_order_label = Label(order_view_frame,text="Products")
products_in_order_label.grid(row=1,column=0)
ok_button = Button(order_view_frame,text="Show",command=show2_table)
ok_button.grid(row=1,column=1)

show_frame(empty_frame)

root.mainloop()