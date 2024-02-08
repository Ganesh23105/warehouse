from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk

def register():
    def clear():
        user_name_entry.delete(0, END)
        user_email_entry.delete(0,END)
        user_password_entry.delete(0,END)
        user_confirm_password_entry.delete(0,END)
    def register_submit():
        if user_name_entry.get()=='' or user_password_entry.get()=='' or user_email_entry.get()=='' or user_confirm_password_entry.get()=='':
            messagebox.showerror('Error','All fields are required.')
        elif user_password_entry.get()!=user_confirm_password_entry.get():
            messagebox.showerror('Error','Password does not match')
        else:
            try:
                con = pymysql.connect(host='localhost',user='root',password='root')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Try Again')
                return 
            try:
                query='create database warehouse'
                mycursor.execute(query)
                query='use warehouse'
                mycursor.execute(query)
                query = 'create table user(user_name VARCHAR(255) NOT NULL PRIMARY KEY,user_password VARCHAR(255) NOT NULL,role VARCHAR(50) NOT NULL,email VARCHAR(255) NOT NULL)'
                mycursor.execute(query)
            except:
                query='use warehouse'
                mycursor.execute(query)

            query = 'select * from user where user_name=%s'
            mycursor.execute(query,(user_name_entry.get()))
            row = mycursor.fetchone()

            if row != None:
                messagebox.showerror('Error','username Already Exists')
            else:
                query = 'insert into user(user_name, email, user_password, role) values(%s,%s,%s,\'admin\')'
                mycursor.execute(query,(user_name_entry.get(),user_email_entry.get(),user_password_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success','Registration is Successful')
                clear()
                registration_window.destroy()
                import employee_page
        
    user_window.destroy()
    registration_window=Tk()
    registration_window.title("REGISTRATION")
    registration_window.geometry("1200x675")

    bgImage = ImageTk.PhotoImage(file='image\\registration.jpg')
    bgLabel=Label(registration_window,image= bgImage)
    bgLabel.place(x=0, y=0)

    sample_Label=Label(registration_window,bg="white")
    sample_Label.place(x=200,y=130)



    user_name_label=Label(sample_Label,text="USER NAME",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
    user_name_label.grid(row=0,column=0,padx=10,pady=10,sticky="e")
    user_name_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
    user_name_entry.grid(row=0,column=1,padx=10,pady=10)    


    user_email_label=Label(sample_Label,text="EMAIL",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
    user_email_label.grid(row=1,column=0,padx=10,pady=10,sticky="e")
    user_email_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
    user_email_entry.grid(row=1,column=1,padx=10,pady=10)

    user_password_label=Label(sample_Label,text="PASSWORD",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
    user_password_label.grid(row=5,column=0,padx=10,pady=10,sticky="e")
    user_password_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
    user_password_entry.grid(row=5,column=1,padx=10,pady=10)

    user_confirm_password_label=Label(sample_Label,text="CONFIRM PASSWORD",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
    user_confirm_password_label.grid(row=6,column=0,padx=10,pady=10,sticky="e")
    user_confirm_password_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
    user_confirm_password_entry.grid(row=6,column=1,padx=10,pady=10)

    user_aadhar_label=Label(sample_Label,text="AADHAR NO",bd=0,font=("Times New Roman",15,"bold"),width=10,bg="white",fg="#163246",activeforeground='#373737')
    user_aadhar_label.grid(row=2,column=0,pady=10,padx=10,sticky="e")
    user_aadhar_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
    user_aadhar_entry.grid(row=2,column=1,pady=10,padx=10)

    user_pan_label=Label(sample_Label,text="PAN NO",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
    user_pan_label.grid(row=3,column=0,padx=10,pady=10,sticky="e")
    user_pan_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
    user_pan_entry.grid(row=3,column=1,padx=10,pady=10)

    user_GST_label=Label(sample_Label,text="GSTIN",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
    user_GST_label.grid(row=4,column=0,padx=10,pady=10,sticky="e")
    user_GST_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
    user_GST_entry.grid(row=4,column=1,padx=10,pady=10)

    user_register_button=Button(sample_Label,text="Register",bd=0,font=("Times New Roman",15,"bold"),bg="#163246",cursor="hand2",fg="white",activeforeground='#373737',command=register_submit)
    user_register_button.grid(row=7,column=0,columnspan=2,pady=20)


    user_name_entry.bind('<Return>',lambda event :user_email_entry.focus())
    user_email_entry.bind('<Return>',lambda event :user_aadhar_entry.focus())
    user_aadhar_entry.bind('<Return>',lambda event :user_pan_entry.focus())
    user_pan_entry.bind('<Return>',lambda event :user_GST_entry.focus())
    user_GST_entry.bind('<Return>',lambda event :user_password_entry.focus())
    user_password_entry.bind('<Return>',lambda event :user_confirm_password_entry.focus())

    registration_window.mainloop()


def login():
    if user_name_entry.get()=='' and user_password_entry.get():
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
        query = 'select * from user where user_name=%s'
        mycursor.execute(query,(user_name_entry.get()))
        row=mycursor.fetchone()

        if row == None:
            messagebox.showerror('Error','INVALID USERNAME')
            return
        else:
            query = 'use warehouse'
            mycursor.execute(query)
            query='SELECT user_password FROM user WHERE user_name=%s'
            mycursor.execute(query,user_name_entry.get())
            sql_password=mycursor.fetchone()
        if user_password_entry.get()!=sql_password[0]:
            messagebox.showerror('ERROR','INVALID PASSWORD')
        else:
            messagebox.showinfo('Success','LOGIN SUCCESSFUL')
            user_window.destroy()
            import employee_page

user_window=Tk()
user_window.geometry('1200x675')
user_window.title("LOGIN")

bgImage = ImageTk.PhotoImage(file='image\\login.jpg')
bgLabel=Label(user_window,image= bgImage)
bgLabel.place(x=0, y=0)

sample_Label=Label(user_window,bg="white")
sample_Label.place(x=250,y=200)

user_name_label=Label(sample_Label,text="USER NAME",bd=0,font=("Times New Roman",18,"bold"),width=10,bg="white",fg="#163246",activeforeground='#373737')
user_name_label.grid(row=0,column=0,pady=(20,10),sticky="w")
user_name_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
user_name_entry.grid(row=0,column=1,pady=(20,10),padx=20)

user_password_label=Label(sample_Label,text="PASSWORD",bd=0,font=("Times New Roman",18,"bold"),width=10,bg="white",fg="#163246",activeforeground='#373737')
user_password_label.grid(row=1,column=0,pady=(10,20),sticky="w")
user_password_entry=Entry(sample_Label,font=("arial"),bd=4,relief=GROOVE)
user_password_entry.grid(row=1,column=1,pady=(10,20))

user_login_button=Button(sample_Label,text="Submit",bd=0,cursor="hand2",font=("Times New Roman",15,"bold"),width=10,bg="#163246",fg="white",activeforeground='#373737',command=login)
user_login_button.grid(row=2,column=0,columnspan=2,pady=20)

register_page_button=Button(sample_Label,text="Not yet Register? Create one",command=register,bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737',cursor="hand2",activebackground="white")
register_page_button.grid(row=3,column=0,pady=20,columnspan=2)



user_name_entry.bind('<Return>',lambda event:user_password_entry.focus())

user_window.mainloop()