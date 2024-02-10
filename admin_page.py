from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import filedialog


def going_to_add():
    search_frame.grid_forget()
    add_frame.grid(row=0,column=8)

def search():
    add_frame.grid_forget()
    search_frame.grid(row=0,column=8)

def upload_photo():
    file_path = filedialog.askopenfilename()
    if file_path:
        uploaded_label = Label(personal_details_Lframe)
        uploaded_label.grid(row=8,column=2)
        image = Image.open(file_path)
        image.thumbnail((50, 50))  
        photo = ImageTk.PhotoImage(image)
        uploaded_label.config(image=photo)
        uploaded_label.image = photo



admin_page=Tk()
admin_page.title("WAREHOUSE")
admin_page.geometry("1200x675")
admin_page.resizable(0,0)

# left frame
admin_page_left_frame=Frame(admin_page)
admin_page_left_frame.place(relx=0,rely=0,relwidth=0.25,relheight=1)

admin_page_left_frame.rowconfigure((0,1,2,3,4),weight=1, uniform = 'a')
admin_page_left_frame.columnconfigure(0,weight=1)

admin_page_left_add_button=Button(admin_page_left_frame,text="ADD",command=going_to_add)
admin_page_left_add_button.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)

admin_page_search_button=Button(admin_page_left_frame,text="SEARCH",command=search)
admin_page_search_button.grid(row=1,column=0,sticky='nsew',padx=10,pady=10)

# right frame

admin_page_right_frame=Frame(admin_page)
admin_page_right_frame.place(relx=0.25,rely=0,relwidth=0.75,relheight=1)

# add frame
add_frame=Frame(admin_page_right_frame)

personal_details_Lframe=LabelFrame(add_frame,text= "Personal Details")
personal_details_Lframe.grid(row=0,column=0)

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
birth_date = DateEntry(personal_details_Lframe)
birth_date.grid(row=3,column=1)

age_label=Label(personal_details_Lframe,text="AGE")
age_label.grid(row=4,column=0)
age_entry=Entry(personal_details_Lframe)
age_entry.grid(row=4,column=1)

contact_no_label=Label(personal_details_Lframe,text="CONTACT NO")
contact_no_label.grid(row=5,column=0)
contact_no_entry=Entry(personal_details_Lframe)
contact_no_entry.grid(row=5,column=1)

email_address_label=Label(personal_details_Lframe,text="EMAIL")
email_address_label.grid(row=6,column=0)
email_address_entry=Entry(personal_details_Lframe)
email_address_entry.grid(row=6,column=1)

    
date_of_joining_label=Label(personal_details_Lframe,text="Date of Joining")
date_of_joining_label.grid(row=7,column=0)
join_date = DateEntry(personal_details_Lframe)
join_date.grid(row=7,column=1)

photo_label=Label(personal_details_Lframe,text="PASSPORT PHOTO")
photo_label.grid(row=8, column=0)
upload_button=Button(personal_details_Lframe,text="UPLOAD",command=upload_photo)
upload_button.grid(row=8,column=1)

submit_button=Button(personal_details_Lframe,text="SUBMIT")
submit_button.grid(row=9,columnspan=2)


# search frame
search_frame=Frame(admin_page_right_frame)


employee_role_label=Label(search_frame,text="ROLE")
employee_role_label.grid(row=0,column=0)
employee_role_entry=Entry(search_frame)
employee_role_entry.grid(row=0,column=1)

employee_username_label=Label(search_frame,text="USERNAME")
employee_username_label.grid(row=1,column=0)
employee_username_entry=Entry(search_frame)
employee_username_entry.grid(row=1,column=1)

employee_year_label=Label(search_frame,text="YEAR")
employee_year_label.grid(row=2,column=0)
employee_year_entry=Entry(search_frame)
employee_year_entry.grid(row=2,column=1)   

employee_month_label=Label(search_frame,text="MONTH")
employee_month_label.grid(row=2,column=4)
employee_month_entry=Entry(search_frame)
employee_month_entry.grid(row=2,column=6) 

employee_reset_button=Button(search_frame,text="RESET")
employee_reset_button.grid(row=3,column=1)

employee_select_button=Button(search_frame,text="SEARCH")
employee_select_button.grid(row=3,column=2)

admin_page.mainloop()