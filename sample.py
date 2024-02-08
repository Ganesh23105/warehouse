# from tkinter import *
# from customtkinter import *
# from tkinter import messagebox
# from PIL import Image,ImageTk

# def stretch_image(event):

#     global resized_tk
#     #size
#     width = event.width
#     height = event.height

#     #create image
#     resized_image = bgOriginal.resize((width,height))
#     resized_tk = ImageTk.PhotoImage(resized_image)

#     #place on the canvas
#     canvas.create_image(0,0, image=resized_tk, anchor='nw')


# def fill_image(event):
#     global resized_tk

#     #current ratio
#     canvas_ratio = event.width / event.height

#     if canvas_ratio > bgRatio :
#         width = int(event.width)
#         height = int(width / bgRatio)

#     else:
#         height = int(event.height)
#         width = int(height * bgRatio)

#     resized_image = bgOriginal.resize((width,height))
#     resized_tk = ImageTk.PhotoImage(resized_image)
#     canvas.create_image(
#         int(event.width /2), 
#         int(event.height)/2, 
#         anchor = 'center', 
#         image = resized_tk)


# def admin_page():
#     select_role.destroy()
#     import admin_login_registration


# def employee_page():
#      select_role.destroy()
#      import employee_login_registration

# select_role=Tk()
# select_role.title("WAREHOUSE")
# select_role.geometry("900x650")
# select_role.resizable(False,False)

# select_role.columnconfigure(0,weight=1)
# select_role.rowconfigure(0,weight=1)

# bgOriginal = Image.open('image\\select_role.jpg')
# bgRatio = bgOriginal.size[0] / bgOriginal.size[1]
# # print(bgRatio)
# bgImage = ImageTk.PhotoImage(bgOriginal)

# canvas = Canvas(select_role,bd=0,highlightthickness=0, relief='ridge')
# canvas.grid(column=0, row=0, sticky='nsew')
# # canvas.create_image(0,0, image=bgImage, anchor='nw')
# canvas.bind('<Configure>',fill_image)

# sample_label = Label(select_role,bg="white")
# sample_label.place(relx=0.75,rely=0.5,anchor=CENTER)

# selection_label=Label(sample_label,text="Select a role",font=("Times New Roman", 40,"bold"),bg="white",fg="#373737")
# selection_label.grid(row=0,column=0,padx=5)

# role_employee_button=Button(sample_label,text="Employee",command=employee_page,bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
# role_employee_button.grid(row=1,column=0,padx=50,pady=20)

# role_admin_button=Button(sample_label,text="Admin",command=admin_page, bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
# role_admin_button.grid(row=3,column=0,padx=50,pady=20)

# select_role.mainloop()
from tkinter import *
import pymysql
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk

student_register_window=Tk()
student_register_window.title("STUDENT REGISTER")
student_register_window.geometry("500x500")

student_fname_label=Label(student_register_window,text="FNAME")
student_fname_label.grid(row=0,column=0,padx=50)
student_fname_entry=Entry(student_register_window)
student_fname_entry.grid(row=1,column=0)

student_mname_label=Label(student_register_window,text="MNAME")
student_mname_label.grid(row=0,column=4,padx=50)
student_mname_entry=Entry(student_register_window)
student_mname_entry.grid(row=1,column=4)  

student_lname_label=Label(student_register_window,text="LNAME")
student_lname_label.grid(row=0,column=8,padx=50)
student_lname_entry=Entry(student_register_window)
student_lname_entry.grid(row=1,column=8)

student_DOB_label=Label(student_register_window,text="DOB",pady=10)
student_DOB_label.grid(row=2,column=0)
student_birth_date = DateEntry(student_register_window)
student_birth_date.grid(row=3,column=0)

student_age_label=Label(student_register_window,text="Age")
student_age_label.grid(row=2,column=4)
student_age_entry=Entry(student_register_window)
student_age_entry.grid(row=3,column=4)

student_phone_number_label=Label(student_register_window,text="Phone Number")
student_phone_number_label.grid(row=4,column=0)
student_phone_number_entry=Entry(student_register_window)
student_phone_number_entry.grid(row=4,column=4,pady=10)

student_college_id_label=Label(student_register_window,text="College ID")
student_college_id_label.grid(row=5,column=0)
student_college_id_entry=Entry(student_register_window)
student_college_id_entry.grid(row=5,column=4,pady=10)

student_college_name_label=Label(student_register_window,text="COLLEGE NAME")
student_college_name_label.grid(row=6,column=0)
student_college_name_entry=Entry(student_register_window)
student_college_name_entry.grid(row=6,column=4,pady=10)

student_college_stream_label=Label(student_register_window,text="STREAM")
student_college_stream_label.grid(row=7,column=0,pady=10)
combo_var_stream=StringVar()
combo_box_stream =ttk.Combobox(student_register_window, textvariable=combo_var_stream)
combo_box_stream['values'] = ('Option 1', 'Option 2', 'Option 3', 'Option 4')
combo_box_stream.grid(row=7,column=4)
combo_box_stream.set("")

student_college_year_label=Label(student_register_window,text="Year")
student_college_year_label.grid(row=9,column=0,pady=10)
combo_var_year=StringVar()
combo_box_year=ttk.Combobox(student_register_window,textvariable=combo_var_year)
combo_box_year['values'] = ('1st year', 'Option 2', 'Option 3', 'Option 4')
combo_box_year.grid(row=9, column=4)
combo_box_year.set("")

student_college_division_label=Label(student_register_window,text="division")
student_college_division_label.grid(row=10,column=0,pady=10)
student_college_division_entry=Entry(student_register_window)
student_college_division_entry.grid(row=10,column=4)

student_college_roll_no_label=Label(student_register_window,text="roll no")
student_college_roll_no_label.grid(row=11,column=0,pady=10)
student_college_roll_no_entry=Entry(student_register_window)
student_college_roll_no_entry.grid(row=11,column=4)

student_submit_button=Button(student_register_window,text="SUBMIT")
student_submit_button.grid(row=14,column=4)





<<<<<<< HEAD

student_register_window.mainloop()
=======
def employee_page():
     select_role.destroy()
     import employee_login_registration

select_role=Tk()
select_role.title("WAREHOUSE")
select_role.geometry("1200x675")
# select_role.resizable(False,False)

select_role.columnconfigure(0,weight=1)
select_role.rowconfigure(0,weight=1)

bgOriginal = Image.open('image\\select_role.jpg')
bgRatio = bgOriginal.size[0] / bgOriginal.size[1]
# print(bgRatio)
bgImage = ImageTk.PhotoImage(bgOriginal)

canvas = Canvas(select_role,bd=0,highlightthickness=0, relief='ridge')
canvas.grid(column=0, row=0, sticky='nsew')
# canvas.create_image(0,0, image=bgImage, anchor='nw')
canvas.bind('<Configure>',fill_image)

sample_label = Label(select_role,bg="white")
sample_label.place(relx=0.75,rely=0.5,anchor=CENTER)

selection_label=Label(sample_label,text="Select a role",font=("Times New Roman", 40,"bold"),bg="white",fg="#373737")
selection_label.grid(row=0,column=0,padx=5)

role_employee_button=Button(sample_label,text="Employee",command=employee_page,bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
role_employee_button.grid(row=1,column=0,padx=50,pady=20)

role_admin_button=Button(sample_label,text="Admin",command=admin_page, bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
role_admin_button.grid(row=3,column=0,padx=50,pady=20)

select_role.mainloop()
>>>>>>> 58ff93e4d8c44e4471232aed5c9e51d093faaf78
