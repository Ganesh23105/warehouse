from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk

def employee_page():
    select_role.destroy()
    import employee_login_registration

def admin_page():
     select_role.destroy()
     import admin_login_registration

select_role=Tk()
select_role.title("WAREHOUSE")
select_role.geometry("900x650")

bgImage = ImageTk.PhotoImage(file='image\\select_role.jpg')
bgLabel=Label(select_role,image= bgImage)
bgLabel.place(x=0, y=0)

sample_label=Label(select_role,background="white")
sample_label.place(x=450,y=200)

sample_label2=Label(sample_label,text="SELECT A ROLE",bg="white",font=("Times New Roman",40,"bold"),fg="#373737")
sample_label2.grid(row=0,column=0,padx=5)

role_admin_button=Button(sample_label,text="EMPLOYEE",command=employee_page, bd=0,font=("Times New Roman",25,"bold"),bg="#373737",cursor="hand2",fg="white",activeforeground='#373737')
role_admin_button.grid(row=1,column=0,padx=50,pady=20)

role_staff_button=Button(sample_label,text="ADMIN",command=admin_page, bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
role_staff_button.grid(row=3,column=0,padx=50,pady=20)

select_role.mainloop()