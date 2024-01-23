from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql


root = Tk()
root.title("Home")
root.geometry("900x650")

left_frame = Frame(root,bg = "lightgray")
left_frame.pack(side=LEFT,fill=Y)

product_Lframe = LabelFrame(left_frame, text="Products")
product_Lframe.grid(row=0,column=0)

order_Lframe = LabelFrame(left_frame,text="Orders")
order_Lframe.grid(row=1,column=0)


right_frame=Frame(root)
right_frame.pack(side=RIGHT,fill=BOTH,expand=True)

# add order

def show1_table():
    if order_id_entry.get()==''or destination_entry.get()=='' or source_entry.get()=='' or products_in_order_entry.get()=='':
        messagebox.showerror('Error','All Fields should be filled.')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='root')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection is not established. Try again.')
            return

        query = 'use warehouse'
        mycursor.execute(query)

        # Check if the "order" table exists, create it if not
        mycursor.execute("SHOW TABLES LIKE 'order'")
        if not mycursor.fetchone():
            query = """
                CREATE TABLE `order` (
                    order_id VARCHAR(225) NOT NULL PRIMARY KEY,
                    source VARCHAR(225) NOT NULL,
                    destination VARCHAR(225) NOT NULL,
                    status VARCHAR(225) NOT NULL
                );
            """
            mycursor.execute(query)

        query = 'SELECT * FROM products WHERE product_id = %s;'
        mycursor.execute(query, products_in_order_entry.get())
        row1 = mycursor.fetchone()

        query = 'SELECT * FROM `order` WHERE order_id = %s;'
        mycursor.execute(query, order_id_entry.get())
        row = mycursor.fetchone()

        if row is not None:
            messagebox.showerror('Error', 'Order id already exists.')
        elif row1 is None:
            messagebox.showerror('Error', 'Product id does not exist.')
        else:

            def on_select(event):
                selected_item = tree.selection()[0]  # Get the selected item (row)
                values = tree.item(selected_item, 'values')

            def submit_this():
                selected_item = tree.selection()[0]
            # print(selected_item)
                values = tree.item(selected_item, 'values')
            # print(values)
                

            
            def add_data(tree, product_id, product_name, location, quantity):
                tree.insert("", "end", values=(product_id, product_name, location, quantity))

            table_frame = Frame(add_order_frame)
            table_frame.grid(row=4, column=0,columnspan=3)

            show_button = Frame(add_order_frame,text="Submit",command=submit_this)
            show_button.grid(row=5, column=0)

            

            tree = ttk.Treeview(table_frame, columns=("Product ID", "Product Name", "Location", "Quantity"), show="headings")

            tree.heading("Product ID", text="Product ID")
            tree.heading("Product Name", text="Product Name")
            tree.heading("Location", text="Location")
            tree.heading("Quantity", text="Quantiy")

            query = 'select * from products where product_id=%s'
            mycursor.execute(query,(products_in_order_entry.get()))
            row2=mycursor.fetchall()

                    
            for i in row2:
                add_data(tree,i[0],i[1],i[2],i[3])

            y_scrollbar = ttk.Scrollbar(add_order_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=y_scrollbar.set)
                
            tree.pack(side="left", fill="both", expand=True)
            y_scrollbar.pack(side="right", fill="y")



add_order_frame = Frame(right_frame)
add_order_frame.pack()

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
ok_button = Button(add_order_frame,text="ADD",command=show1_table)
ok_button.grid(row=3,column=2)






root.mainloop()