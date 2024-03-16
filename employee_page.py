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

def database_add_products():
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

def order_view():
    add_frame.pack_forget()
    hide_frame(add_order_frame)
    hide_frame(view_product_frame)
    show_frame(order_view_frame)

def order_add():
    hide_frame(order_view_frame)
    add_frame.pack_forget()
    hide_frame(view_product_frame)
    show_frame(add_order_frame)

def view_product():
    hide_frame(order_view_frame)
    add_frame.pack_forget()
    hide_frame(add_order_frame)
    show_frame(view_product_frame)
    
def add_product():
    hide_frame(order_view_frame)
    hide_frame(view_product_frame)
    hide_frame(add_order_frame)
    add_frame.place(relx=0.025,rely=0.05,relwidth=0.95,relheight=0.9)

def show_frame(frame):
    frame.place(relx=0.5,rely=0.5,anchor='center')

def hide_frame(frame):
    frame.place_forget()

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

location_label=Label(add_frame,text="LOCATION")
location_label.grid(row=2,column=0)
location_entry=Entry(add_frame)
location_entry.grid(row=2,column=1)

quantity_label=Label(add_frame,text="QUANTITY")
quantity_label.grid(row=3,column=0)
quantity_entry=Entry(add_frame)
quantity_entry.grid(row=3,column=1)

submit_button=Button(add_frame,text="SUBMIT",command=database_add_products)
submit_button.grid(row=4,column=0,columnspan=2)

product_id_entry.bind('<Return>',lambda event :product_name_entry.focus())
product_name_entry.bind('<Return>',lambda event :location_entry.focus())
location_entry.bind('<Return>',lambda event :quantity_entry.focus())

#retrieve product 
view_product_frame=Frame(right_frame)

combo_var_stream=StringVar()
combo_box_stream =ttk.Combobox(view_product_frame,textvariable=combo_var_stream,state="readonly")
combo_box_stream['values'] = ('Product ID', 'Product Name', 'Location')
combo_box_stream.grid(row=0,column=0)
combo_box_stream.set("Select")

entryfield_entry=Entry(view_product_frame)
entryfield_entry.grid(row=0,column=1)

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

        table_frame = Frame(view_product_frame)
        table_frame.grid(row=1, column=0,columnspan=3)

        change_button = Button(view_product_frame, text="Change Selected Row", command=change_selected_row)
        change_button.grid(row=2, column=0,columnspan=3)

        tree = ttk.Treeview(table_frame, columns=("Product ID", "Product Name", "Location","Quantity"), show="headings")

        tree.heading("Product ID", text="Product ID")
        tree.heading("Product Name", text="Product Name")
        tree.heading("Location", text="Location")
        tree.heading("Quantity", text="Quantity")
                
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

show_button=Button(view_product_frame,text="SHOW",font=10,width=8,bg="white",fg="#033043",cursor="hand2",command=show_table)
show_button.grid(row=0,column=2)


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