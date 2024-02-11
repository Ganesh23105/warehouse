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