from tkinter import *
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk
import ttkthemes

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
    show2_table

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

    # Check if any item is selected in the treeview
    if not view_product_tree.selection():
        messagebox.showerror('Error', 'Please select an item from the list.')
        return
    
    selected_item = view_product_tree.selection()[0]
    # print(selected_item)
    values = view_product_tree.item(selected_item, 'values')
    # print(values)

    def products_updation():
        try:
            con = pymysql.connect(host='localhost',user='root',password='root',database='warehouse')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again.')
            return

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

product_add_button=CTkButton(product_Lframe,text="ADD",command=add_product,width=100,height=20,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_add_button.grid(row=0,column=0)

product_view_button=CTkButton(product_Lframe,text="VIEW",command=view_product,width=100,height=20,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_view_button.grid(row=1,column=0)

#order Lframe
order_Lframe = LabelFrame(left_frame,text="Orders")
order_Lframe.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")
order_Lframe.columnconfigure(0,weight=1)


order_add_button=CTkButton(order_Lframe,text="ADD",command=order_add,width=100,height=20,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
order_add_button.grid(row=0,column=0)

order_view_button=CTkButton(order_Lframe,text="VIEW",command=order_view,width=100,height=20,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
order_view_button.grid(row=1,column=0)

right_frame=Frame(root,bg ="#E9E3D5")
right_frame.place(relx=0.2,rely=0,relwidth=0.8,relheight=1)

# add button in products

add_frame = Frame(right_frame,borderwidth=5,relief='groove',bg="white")

product_id_label=CTkLabel(add_frame,text="PRODUCT ID",width=150,height=10,corner_radius=12,font=("Times New Roman",15,"bold"),fg_color='#373737',text_color='#e9e3d5')
product_id_label.grid(row=0,column=0)
product_id_entry=CTkEntry(add_frame,width=120,height=10,corner_radius=10.5,border_color='#373737',fg_color='#e9e3d5',text_color='#373737',font=("Times New Roman",14,"bold"))
product_id_entry.grid(row=0,column=1)

product_name_label=CTkLabel(add_frame,text="PRODUCT NAME",width=150,height=10,corner_radius=12,font=("Times New Roman",15,"bold"),fg_color='#373737',text_color='#e9e3d5')
product_name_label.grid(row=1,column=0)
product_name_entry=CTkEntry(add_frame,width=120,height=10,corner_radius=10.5,border_color='#373737',fg_color='#e9e3d5',text_color='#373737',font=("Times New Roman",14,"bold"))
product_name_entry.grid(row=1,column=1)

brand_nt, category_nt = combo_group_by()
brand_values_view_frame = flatten_tuple(brand_nt)
brand_values_add_frame = flatten_tuple(brand_nt)
category_values_view_frame = flatten_tuple(category_nt)
category_values_add_frame = flatten_tuple(category_nt)

brand_values_add_frame.append('NEW')
category_values_add_frame.append('NEW')

brand_values_view_frame.append('NONE')
category_values_view_frame.append('NONE')

product_brand_label=CTkLabel(add_frame,text="BRAND",width=150,height=10,corner_radius=12,font=("Times New Roman",15,"bold"),fg_color='#373737',text_color='#e9e3d5')
product_brand_label.grid(row=2,column=0)
brand_combobox_var=StringVar()
brand_combobox =ttk.Combobox(add_frame,textvariable=brand_combobox_var,state="readonly")
brand_combobox['values'] = brand_values_add_frame
brand_combobox.grid(row=2,column=1)
brand_combobox.set("SELECT")
brand_combobox.bind("<<ComboboxSelected>>", enable_entry)
product_brand_entry=Entry(add_frame, state='readonly')
product_brand_entry.grid(row=2,column=2)

product_category_label=CTkLabel(add_frame,text="CATEGORY",width=150,height=10,corner_radius=12,font=("Times New Roman",15,"bold"),fg_color='#373737',text_color='#e9e3d5')
product_category_label.grid(row=3,column=0)
category_combobox_var=StringVar()
category_combobox =ttk.Combobox(add_frame,textvariable=category_combobox_var,state="readonly")
category_combobox['values'] = category_values_add_frame
category_combobox.grid(row=3,column=1)
category_combobox.set("SELECT")
category_combobox.bind("<<ComboboxSelected>>", enable_entry)
product_category_entry=Entry(add_frame, state='readonly')
product_category_entry.grid(row=3,column=2)

location_label=CTkLabel(add_frame,text="LOCATION",width=150,height=10,corner_radius=12,font=("Times New Roman",15,"bold"),fg_color='#373737',text_color='#e9e3d5')
location_label.grid(row=4,column=0)
location_entry=Entry(add_frame)
location_entry.grid(row=4,column=1)

quantity_label=CTkLabel(add_frame,text="QUANTITY",width=150,height=10,corner_radius=12,font=("Times New Roman",15,"bold"),fg_color='#373737',text_color='#e9e3d5')
quantity_label.grid(row=5,column=0)
quantity_entry=Entry(add_frame)
quantity_entry.grid(row=5,column=1)

submit_button=Button(add_frame,text="SUBMIT",command=database_add_products)
submit_button.grid(row=6,column=0,columnspan=2)

#view product 
view_product_frame=Frame(right_frame)

view_product_attributes_frame = Frame(view_product_frame,bg="white")
view_product_attributes_frame.place(relx=0,rely=0,relwidth=1,relheight=0.15)
view_product_attributes_frame.rowconfigure(0,weight=1)
view_product_attributes_frame.columnconfigure((0,1,2,3,4,5),weight=1)

select_type_combobox_var=StringVar(value="SELECT")
select_type_combobox=CTkComboBox(view_product_attributes_frame,variable=select_type_combobox_var,
                                  values=['Product ID', 'Product Name', 'Location'],
                                  width=140,height=40,
								   corner_radius=15,
								   fg_color='#e9e3d5',text_color='#373737',
								   border_color='#373737',
								   button_color='#373737',
								   font=("Times New Roman",12,"bold"),
								   button_hover_color='#e9e3d5',
								   dropdown_fg_color='white',
								   dropdown_hover_color='#e9e3d5',
								   dropdown_font=("Times New Roman",15,"bold"),
								   dropdown_text_color='#373737',
								   justify='center',
								   state='readonly',
								   border_width=3)

select_type_combobox.grid(row=0,column=0)
select_type_combobox.set("SELECT")

select_type_entry=CTkEntry(view_product_attributes_frame,width=185,height=35,corner_radius=10.5,border_color='#373737',fg_color='#e9e3d5',text_color='#373737',font=("Times New Roman",14,"bold"))
select_type_entry.grid(row=0,column=1) 

brand_label=CTkLabel(view_product_attributes_frame,text="BRAND",fg_color="#373737",font=("Times New Roman",20,"bold"),text_color="#e9e3d5",corner_radius=10)
brand_label.grid(row=0,column=2)

view_brand_combobox_var=StringVar(value="SELECT")
view_brand_combobox =CTkComboBox(view_product_attributes_frame,variable=view_brand_combobox_var,
                                 values= brand_values_view_frame,
                                width=140,height=40,
								corner_radius=15,
								fg_color='#e9e3d5',text_color='#373737',
								border_color='#373737',
								button_color='#373737',
								font=("Times New Roman",12,"bold"),
								button_hover_color='#e9e3d5',
								dropdown_fg_color='white',
								dropdown_hover_color='#e9e3d5',
								dropdown_font=("Times New Roman",15,"bold"),
								dropdown_text_color='#373737',
								justify='center',
								state='readonly',
								border_width=3)

# view_brand_combobox['values'] = flatten_tuple(brand_nt)

view_brand_combobox.grid(row=0,column=3)
view_brand_combobox.set("SELECT")

category_label=CTkLabel(view_product_attributes_frame,text="CATEGORY",fg_color="#373737",font=("Times New Roman",20,"bold"),text_color="#e9e3d5",corner_radius=10)
category_label.grid(row=0,column=4)
view_category_combobox_var=StringVar(value="SELECT")
view_category_combobox =CTkComboBox(view_product_attributes_frame,variable=view_category_combobox_var,
                                    values= category_values_view_frame,
                                    width=140,height=40,
								    corner_radius=15,
								    fg_color='#e9e3d5',text_color='#373737',
								    border_color='#373737',
								    button_color='#373737',
								    font=("Times New Roman",12,"bold"),
								    button_hover_color='#e9e3d5',
								    dropdown_fg_color='white',
								    dropdown_hover_color='#e9e3d5',
								    dropdown_font=("Times New Roman",15,"bold"),
								    dropdown_text_color='#373737',
								    justify='center',
								    state='readonly',
								    border_width=3)
# view_category_combobox['values'] = flatten_tuple(category_nt)
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

style=ttkthemes.ThemedStyle(view_product_tree)

style.theme_use('clam')
style.configure('Treeview',font=("Times New Roman",10),foreground='black',background="white")
style.configure('Treeview.Heading',font=("Times New Roman",10,"bold"),foreground='#e9e3d5',background='#373737')
style.map("Treeview", background= [('selected','#e9e3d5')], foreground= [('selected','#373737')])
style.map("Treeview.Heading", background= [('selected','#373737')], foreground= [('selected','#e9e3d5')])

        
view_product_button_frame = Frame(view_product_frame,bg="white")
view_product_button_frame.place(relx=0,rely=0.85,relheight=0.15,relwidth=1)
view_product_button_frame.rowconfigure(0,weight=1)
view_product_button_frame.columnconfigure((0,1,2,3),weight=1)

def view_product_reset():
    view_category_combobox.set("SELECT")
    view_brand_combobox.set("SELECT")
    select_type_combobox.set("SELECT")
    select_type_entry.delete(0,END)
    retrieve_product_data()

product_reset_button=CTkButton(view_product_button_frame,text="RESET",command=view_product_reset,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_reset_button.grid(row=0,column=0)

def search_product():
    # for item in view_product_tree.get_children():
    #     view_product_tree.delete(item)

    if select_type_entry.get()=='' and (view_brand_combobox.get()=='SELECT' or view_brand_combobox.get()=='NONE') and (view_category_combobox.get()=='SELECT' or view_category_combobox.get()=='NONE'):
        messagebox.showerror('Error','All Fields should be filled.')
    else:
        try:
            con = pymysql.connect(host='localhost',user='root',password='root',database='warehouse')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again.')
            return
        flag=0
        string=""
        lst=[]
                
        if select_type_combobox.get()=='Product ID' and select_type_entry.get()!='':
            string = 'product_id = %s'
            lst.append(select_type_entry.get())
            flag=1
        elif select_type_combobox.get()=="Product Name" and select_type_entry.get()!='':
            string = 'product_name = %s'
            lst.append(select_type_entry.get())
            flag=1
        elif select_type_combobox.get()=="Location" and select_type_entry.get()!='':
            string = 'location = %s'
            lst.append(select_type_entry.get())
            flag=1

        if view_brand_combobox.get()!='SELECT' and view_brand_combobox.get()!='NONE':
            lst.append(view_brand_combobox.get())
            if flag==1:
                string+=" and brand=%s"
            else:
                string+="brand=%s"
            flag=2

        if view_category_combobox.get()!='SELECT' and view_category_combobox.get()!='NONE':
            lst.append(view_category_combobox.get())
            if flag==1 or flag==2:
                string+=" and category=%s"
            else:
                string+="category=%s"
            # flag=0

        query="select * from products where " + string
        # print(query)
        # print(tuple(lst))
        mycursor.execute(query,tuple(lst))
        fetch_row = mycursor.fetchall()
        for item in view_product_tree.get_children():
            view_product_tree.delete(item)
        for i in fetch_row:
            view_product_tree.insert("", "end", values=(i[0], i[1], i[4], i[5],i[2],i[3]))

product_search_button=CTkButton(view_product_button_frame,text="SEARCH",command=search_product,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_search_button.grid(row=0,column=1)



product_view_button=CTkButton(view_product_button_frame,text="VIEW",command=change_selected_row,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_view_button.grid(row=0,column=2)

product_barcode_button=CTkButton(view_product_button_frame,text="BARCODE",width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
product_barcode_button.grid(row=0,column=3)

# bgfImage= ImageTk.PhotoImage(file='image\\4.2.jpg')
empty_frame = Frame(right_frame)

# image_label=Label(empty_frame,image=bgfImage)
# image_label.pack(side=RIGHT,fill=BOTH,expand=True)

# add order
add_order_frame = Frame(right_frame,borderwidth=5,relief='groove',bg="white")

add_order_attributes_frame = Frame(add_order_frame,bg="white")
add_order_attributes_frame.place(relx=0,rely=0,relwidth=0.75,relheight=0.15)
add_order_attributes_frame.rowconfigure(0,weight=1,uniform='a')
add_order_attributes_frame.columnconfigure((0,1),weight=4,uniform='a')
add_order_attributes_frame.columnconfigure((2,3),weight=5,uniform='a')

select_type_combobox_order_var=StringVar(value="SELECT")
select_type_combobox_order=CTkComboBox(add_order_attributes_frame,variable=select_type_combobox_order_var,
                                  values=['Product ID', 'Product Name', 'Location'],
                                  width=140,height=40,
								   corner_radius=15,
								   fg_color='#e9e3d5',text_color='#373737',
								   border_color='#373737',
								   button_color='#373737',
								   font=("Times New Roman",12,"bold"),
								   button_hover_color='#e9e3d5',
								   dropdown_fg_color='white',
								   dropdown_hover_color='#e9e3d5',
								   dropdown_font=("Times New Roman",15,"bold"),
								   dropdown_text_color='#373737',
								   justify='center',
								   state='readonly',
								   border_width=3)

select_type_combobox_order.grid(row=0,column=0,sticky='nsew',padx=5,pady=25) 
select_type_combobox_order.set("SELECT")

select_type_order_entry=CTkEntry(add_order_attributes_frame,width=140,height=40,corner_radius=10.5,border_color='#373737',fg_color='#e9e3d5',text_color='#373737',font=("Times New Roman",14,"bold"))
select_type_order_entry.grid(row=0,column=1,sticky='nsew',padx=5,pady=25) 

brandorder_label=LabelFrame(add_order_attributes_frame,text="BRAND",bg="white",font=("Times New Roman",10,"bold"),fg="#373737")
brandorder_label.grid(row=0,column=2,sticky='nsew',padx=(0,10),pady=5)

add_brand_order_combobox_var=StringVar(value="SELECT")
add_brand_order_combobox =CTkComboBox(brandorder_label,variable=add_brand_order_combobox_var,
                                 values= brand_values_view_frame,
                                width=160,height=40,
								corner_radius=10,
								fg_color='#e9e3d5',text_color='#373737',
								border_color='#373737',
								button_color='#373737',
								font=("Times New Roman",12,"bold"),
								button_hover_color='#e9e3d5',
								dropdown_fg_color='white',
								dropdown_hover_color='#e9e3d5',
								dropdown_font=("Times New Roman",15,"bold"),
								dropdown_text_color='#373737',
								justify='center',
								state='readonly',
								border_width=3)
add_brand_order_combobox.pack(expand=True)
add_brand_order_combobox.set("SELECT")

category_order_label=LabelFrame(add_order_attributes_frame,text="CATEGORY",bg="white",font=("Times New Roman",10,"bold"),fg="#373737")
category_order_label.grid(row=0,column=3,sticky='nsew',padx=(0,10),pady=5)
add_category_order_combobox_var=StringVar(value="SELECT")
add_category_order_combobox =CTkComboBox(category_order_label,variable=add_category_order_combobox_var,
                                    values= category_values_view_frame,
                                    width=160,height=40,
								    corner_radius=10,
								    fg_color='#e9e3d5',text_color='#373737',
								    border_color='#373737',
								    button_color='#373737',
								    font=("Times New Roman",12,"bold"),
								    button_hover_color='#e9e3d5',
								    dropdown_fg_color='white',
								    dropdown_hover_color='#e9e3d5',
								    dropdown_font=("Times New Roman",15,"bold"),
								    dropdown_text_color='#373737',
								    justify='center',
								    state='readonly',
								    border_width=3)
add_category_order_combobox.pack(expand=True)
add_category_order_combobox.set("SELECT")

add_order_table_products_frame = Frame(add_order_frame)
add_order_table_products_frame.place(relx=0,rely=0.15,relwidth=0.75,relheight=0.47)

add_order_product_tree = ttk.Treeview(add_order_table_products_frame, columns=("Product ID", "Product Name", "Quantity","Location","Brand","Category"), show="headings",height=100)

add_order_product_tree.heading("Product ID", text="Product ID")
add_order_product_tree.heading("Product Name", text="Product Name")
add_order_product_tree.heading("Quantity", text="Quantiy")
add_order_product_tree.heading("Location", text="Location")
add_order_product_tree.heading("Brand", text="Brand")
add_order_product_tree.heading("Category",text="Category")

add_order_product_y_scrollbar = Scrollbar(add_order_table_products_frame, orient="vertical", command=add_order_product_tree.yview)
add_order_product_tree.configure(yscrollcommand=add_order_product_y_scrollbar.set)
add_order_product_y_scrollbar.pack(side='right',fill=Y)

add_order_product_x_scrollbar = Scrollbar(add_order_table_products_frame, orient="horizontal", command=add_order_product_tree.xview)
add_order_product_tree.configure(xscrollcommand=add_order_product_x_scrollbar.set)
add_order_product_x_scrollbar.pack(side='bottom',fill=X)
        
add_order_product_tree.pack()

##
add_order_buttons_frame = CTkFrame(add_order_frame,fg_color="#e9e3d5",corner_radius=15)
add_order_buttons_frame.place(relx=0.76,rely=0.01,relwidth=0.23,relheight=0.24)
add_order_buttons_frame.rowconfigure((0,1,2),weight=1,uniform='a')
add_order_buttons_frame.columnconfigure((0),weight=1,uniform='a')

employee_barcode_button=CTkButton(add_order_buttons_frame,text="BARCODE",width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
employee_barcode_button.grid(row=0,column=0)

employee_search_button=CTkButton(add_order_buttons_frame,text="SEARCH",width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
employee_search_button.grid(row=1,column=0)

employee_reset_button=CTkButton(add_order_buttons_frame,text="RESET",width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
employee_reset_button.grid(row=2,column=0)

add_order_quantity_frame = CTkFrame(add_order_frame,fg_color="#e9e3d5",corner_radius=15)
add_order_quantity_frame.place(relx=0.76,rely=0.26,relwidth=0.23,relheight=0.36)
add_order_quantity_frame.rowconfigure((0,1),weight=3,uniform='a')
add_order_quantity_frame.rowconfigure((2),weight=2,uniform='a')
add_order_quantity_frame.columnconfigure((0),weight=1,uniform='a')

product_id_order_labelFrame=LabelFrame(add_order_quantity_frame,text="PRODUCT ID",bg="#E9E3D5",font=("Times New Roman",10,"bold"),fg="black")
product_id_order_labelFrame.grid(row=0,column=0,sticky='nsew',padx=5,pady=(0,5))

product_id_order_entry=CTkEntry(product_id_order_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
product_id_order_entry.pack(expand=TRUE) 

quantity_order_labelFrame=LabelFrame(add_order_quantity_frame,text="QUANTITY",bg="#E9E3D5",font=("Times New Roman",10,"bold"),fg="black")
quantity_order_labelFrame.grid(row=1,column=0,sticky='nsew',padx=5)

quantity_order_entry=CTkEntry(quantity_order_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
quantity_order_entry.pack(expand=TRUE) 

add_product_button=CTkButton(add_order_quantity_frame,text="ADD",width=100,height=20,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
add_product_button.grid(row=2,column=0)

##
add_order_main_attributes_frame = CTkFrame(add_order_frame,fg_color="#e9e3d5",corner_radius=15)
add_order_main_attributes_frame.place(relx=0.01,rely=0.63,relwidth=0.23,relheight=0.36)
add_order_main_attributes_frame.rowconfigure((0,1,2),weight=1,uniform='a')
# add_order_main_attributes_frame.rowconfigure((2),weight=5,uniform='a')
add_order_main_attributes_frame.columnconfigure((0),weight=1,uniform='a')

order_id_order_labelFrame=LabelFrame(add_order_main_attributes_frame,text="ORDER ID",bg="#E9E3D5",font=("Times New Roman",10,"bold"),fg="black")
order_id_order_labelFrame.grid(row=0,column=0,sticky='nsew',padx=5,pady=(0,5))

order_id_order_entry=CTkEntry(order_id_order_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
order_id_order_entry.pack(expand=TRUE) 

customer_order_labelFrame=LabelFrame(add_order_main_attributes_frame,text="CUSTOMER",bg="#E9E3D5",font=("Times New Roman",10,"bold"),fg="black")
customer_order_labelFrame.grid(row=1,column=0,sticky='nsew',padx=5)

customer_order_entry=CTkEntry(customer_order_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
customer_order_entry.pack(expand=TRUE) 

def order_submit():
        if order_id_entry.get()=='' and customer_order_entry.get()=='':
            messagebox.showerror('Error',"Please fill all the details.")
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
                create_query="create table `order`(orderid VARCHAR(255) NOT NULL PRIMARY KEY,customer VARCHAR(255) NOT NULL)"
                mycursor.execute(create_query)
            except:
                pass

            check_order_id_query = 'select * from `order` where orderid = %s'
            mycursor.execute(check_order_id_query,order_id_order_entry.get())
            row = mycursor.fetchone()
            print(row)

            if row!=None:
                messagebox.showerror('Error', 'Order ID '+order_id_order_entry.get()+' already exists.')
            else:
                query="insert into `order`(orderid,customer) values(%s,%s)"
                mycursor.execute(query,(order_id_order_entry.get(),customer_order_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success','Order '+order_id_order_entry.get()+' successfully added!')
                clear()
                
submit_product_button=CTkButton(add_order_main_attributes_frame,text="SUBMIT",command=order_submit,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
submit_product_button.grid(row=2,column=0)

##
add_order_table_bill_frame = Frame(add_order_frame)
add_order_table_bill_frame.place(relx=0.25,rely=0.62,relwidth=0.75,relheight=0.38)

add_order_bill_tree = ttk.Treeview(add_order_table_bill_frame, columns=("Product ID", "Product Name", "Quantity","Brand","Category"), show="headings",height=100)

add_order_bill_tree.heading("Product ID", text="Product ID")
add_order_bill_tree.heading("Product Name", text="Product Name")
add_order_bill_tree.heading("Quantity", text="Quantiy")
add_order_bill_tree.heading("Brand", text="Brand")
add_order_bill_tree.heading("Category",text="Category")

add_order_bill_y_scrollbar = Scrollbar(add_order_table_bill_frame, orient="vertical", command=add_order_bill_tree.yview)
add_order_bill_tree.configure(yscrollcommand=add_order_bill_y_scrollbar.set)
add_order_bill_y_scrollbar.pack(side='right',fill=Y)

add_order_bill_x_scrollbar = Scrollbar(add_order_table_bill_frame, orient="horizontal", command=add_order_bill_tree.xview)
add_order_bill_tree.configure(xscrollcommand=add_order_bill_x_scrollbar.set)
add_order_bill_x_scrollbar.pack(side='bottom',fill=X)
        
add_order_bill_tree.pack()

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
ok_button = Button(order_view_frame,text="Show")
ok_button.grid(row=1,column=1)

show_frame(empty_frame)

root.mainloop()