from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk
from tkcalendar import DateEntry



def going_to_add():
    admin_page_right_frame=Frame(admin_page,bg="blue")
    admin_page_right_frame.grid(row=0,column=6)

    # product_Lframe = LabelFrame(left_frame, text="Products",font=("Poppins",12,"bold"))
    # product_Lframe.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")
    personal_details_Lframe=LabelFrame(admin_page_right_frame,text= "Personal Details")
    personal_details_Lframe.grid(row=0,column=0)

    # quantity_label=Label(add_frame,text="QUANTITY",bd=0,font=("Times New Roman",15,"bold"),bg="white",fg="#163246",activeforeground='#373737')
    # quantity_label.grid(row=3,column=0,padx=10,pady=10,sticky="e")
    # quantity_entry=Entry(add_frame,bd=4,relief=GROOVE)
    # quantity_entry.grid(row=3,column=1,padx=10,pady=10)

    first_name_label=Label(personal_details_Lframe,text="FIRST NAME")
    first_name_label.grid(row=0,column=0)
    first_name_entry=Entry(personal_details_Lframe)
    first_name_entry.grid(row=0,column=1)

    middle_name_label=Label(personal_details_Lframe,text="MIDDLE NAME")
    middle_name_label.grid(row=1,column=0)
    middle_name_entry=Entry(personal_details_Lframe)
    middle_name_entry.grid(row=1,column=1)

    last_name_label=Label(personal_details_Lframe,text="LAST NAME")
    last_name_label.grid(row=2,column=0)
    last_name_entry=Entry(personal_details_Lframe)
    last_name_entry.grid(row=2,column=1)

    date_of_birth_label=Label(personal_details_Lframe,text="Date of Birth")
    date_of_birth_label.grid(row=3,column=0)
    student_DOB_label=Label(student_register_window,text="DOB",pady=10)
    student_DOB_label.grid(row=2,column=0)
    student_birth_date = DateEntry(student_register_window)
    student_birth_date.grid(row=3,column=0)



admin_page=Tk()
admin_page.title("WAREHOUSE")
admin_page.geometry("1200x675")
admin_page.resizable(0,0)

# left frame
admin_page_left_frame=Frame(admin_page)
admin_page_left_frame.grid(row=0,column=5)

admin_page_left_add_button=Button(admin_page_left_frame,text="ADD",command=going_to_add)
admin_page_left_add_button.grid(row=0,column=0)

admin_page_search_button=Button(admin_page_left_frame,text="SEARCH")
admin_page_search_button.grid(row=1,column=0)
# right frame

# admin_page_right_frame=Frame(admin_page,bg="blue")
# admin_page_right_frame.grid(row=0,column=6)


# admin_page_search_button=Button(admin_page_right_frame,text="hi")
# admin_page_search_button.grid(row=0,column=0)










admin_page.mainloop()