from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk

def fill_image(event):
	global resized_tk

	# current ratio 
	canvas_ratio = event.width / event.height

	# get coordinates 
	if canvas_ratio > image_ratio: # canvas is wider than the image
		width = int(event.width) 
		height = int(width / image_ratio)
	else: # canvas is narrower than the image
		height = int(event.height)
		width = int(height * image_ratio) 

	resized_image = image_original.resize((width, height))
	resized_tk = ImageTk.PhotoImage(resized_image)
	canvas.create_image(
		int(event.width / 2),
		int(event.height / 2),
		anchor = 'center',
		image = resized_tk)

def login():
    if user_name_entry.get()=="" or user_password_entry.get()=="":
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
        if user_password_entry.get()!=sql_password[0]:
            messagebox.showerror('ERROR','INVALID PASSWORD')
        else:
            messagebox.showinfo('Success','LOGIN SUCCESSFUL')
            user_window.destroy()
            import employee_page

user_window=Tk()
user_window.geometry('1200x675')
user_window.minsize(800,450)
user_window.title("LOGIN")

user_window.columnconfigure(0, weight = 1, uniform = 'a')
user_window.rowconfigure(0, weight = 1)

# import an image 
image_original = Image.open('image\\login.jpg')
image_ratio = image_original.size[0] / image_original.size[1]
image_tk = ImageTk.PhotoImage(image_original)

canvas = Canvas(user_window, background = 'black', bd = 0, highlightthickness = 0, relief = 'ridge')
canvas.grid(column = 0, row = 0, sticky = 'nsew')

canvas.bind('<Configure>', fill_image)

sample_Label=Label(user_window,bg="white")
sample_Label.place(relx=0.5,rely=0.5,anchor=CENTER,relwidth=0.4,relheight=0.5)
sample_Label.rowconfigure((0,3),weight=2,uniform="b")
sample_Label.rowconfigure((1,2),weight=1,uniform="a")
sample_Label.columnconfigure((0,1),weight=1,uniform="A")

login_heading_label=Label(sample_Label,text="LOGIN",bd=0,font=("Times New Roman",50,"bold"),bg="white",fg="#373737")
login_heading_label.grid(row=0,column=0,columnspan=2)

user_name_label=Label(sample_Label,text="USER NAME",bd=0,font=("Times New Roman",18,"bold"),width=10,bg="white",fg="#373737",activeforeground='#373737')
user_name_label.grid(row=1,column=0,sticky="nsew")
user_name_entry=Entry(sample_Label,font=("arial",13),bd=4,relief=GROOVE,width=20)
user_name_entry.grid(row=1,column=1,sticky='w')

user_password_label=Label(sample_Label,text="PASSWORD",bd=0,font=("Times New Roman",18,"bold"),width=10,bg="white",fg="#373737",activeforeground='#373737')
user_password_label.grid(row=2,column=0,sticky="nsew")
user_password_entry=Entry(sample_Label,font=("arial",13),bd=4,relief=GROOVE,width=20)
user_password_entry.grid(row=2,column=1,sticky='w')

user_login_button=Button(sample_Label,text="SUBMIT",bd=0,cursor="hand2",font=("Times New Roman",20,"bold"),width=12,bg="#373737",fg="white",activeforeground='#373737',command=login)
user_login_button.grid(row=3,column=0,columnspan=2,sticky='nsew',padx=175,pady=30)


user_name_entry.bind('<Return>',lambda event:user_password_entry.focus())

user_window.mainloop()
