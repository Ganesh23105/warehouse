from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk


# user_window.destroy()
admin_login_registration=Tk()
admin_login_registration.title("ADMIN REGISTRATION")
admin_login_registration.geometry("1200x675")
admin_login_registration.minsize(800,450)

def admin_page():
    if user_name_entry.get()=='' and password_entry.get():
        messagebox.showerror("ERROR","All fields should be filled.")
    else:
        try:
            con = pymysql.connect(host='localhost',user='root',password='root')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again.')
            return

        query = 'use warehouse'
        mycursor.execute(query)
        query = 'select * from user where username=%s'
        mycursor.execute(query,(user_name_entry.get()))
        row=mycursor.fetchone()

        if row == None:
            messagebox.showerror('Error','INVALID USERNAME')
            return
        else:
            query = 'use warehouse'
            mycursor.execute(query)
            query='SELECT password FROM user WHERE username=%s'
            mycursor.execute(query,user_name_entry.get())
            sql_password=mycursor.fetchone()
        if password_entry.get()!=sql_password[0]:
            messagebox.showerror('ERROR','INVALID PASSWORD')
        else:
            messagebox.showinfo('Success','LOGIN SUCCESSFUL')
            admin_login_registration.destroy()
            import admin_page


bgImage = ImageTk.PhotoImage(file='image\\login.jpg')
bgLabel=Label(admin_login_registration,image= bgImage)
bgLabel.place(x=0, y=0)

sample_Label=Label(admin_login_registration,bg="white")
sample_Label.place(x=250,y=230)

user_name_label=Label(sample_Label,text="USER NAME",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
user_name_label.grid(row=0,column=0,padx=10,pady=10,sticky="e")
user_name_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
user_name_entry.grid(row=0,column=1,padx=10,pady=10) 

password_label=Label(sample_Label,text="PASSWORD",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
password_label.grid(row=1,column=0,padx=10,pady=10,sticky="w")
password_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
password_entry.grid(row=1,column=1,padx=10,pady=10)

Login_button=Button(sample_Label,text="Login",bd=0,font=("Times New Roman",15,"bold"),bg="#163246",cursor="hand2",fg="white",activeforeground='#373737',command=admin_page,width=13)
Login_button.grid(row=3,column=0,columnspan=2,pady=20)

user_name_entry.bind("<Return>",lambda event:password_entry.focus())

admin_login_registration.mainloop()
    
