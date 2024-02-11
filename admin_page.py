from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import filedialog
from datetime import datetime, timedelta
import secrets
import string


def generate_username():
    try:
        con = pymysql.connect(host='localhost',user='root',password='root',database='warehouse')
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error','Database Connectivity Issue, Try Again')
        return

    fname = first_name_entry.get()
    mname = middle_name_entry.get()
    lname = last_name_entry.get()
    eighteen_years_ago = now_date()
    username = role_combo_box.get()[0] + fname[0].lower() + mname[0].lower() + lname[0].lower() + str(eighteen_years_ago.year)

    check_username_query = 'select username from user where username = %s'
    mycursor.execute(check_username_query,username)
    row = mycursor.fetchone()
    if row == None:
        return username

def generate_password():
    # Define character sets
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digit_chars = string.digits
    punctuation_chars = string.punctuation

    # Generate components of the password
    lowercase_part = ''.join(secrets.choice(lowercase_chars) for _ in range(4))
    uppercase_part = secrets.choice(uppercase_chars)
    digit_part = ''.join(secrets.choice(digit_chars) for _ in range(2))
    punctuation_part = secrets.choice(punctuation_chars)

    # Combine components to form the password
    password = lowercase_part + uppercase_part + digit_part + punctuation_part

    # Shuffle the password to make it more secure
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    shuffled_password = ''.join(password_list)

    return shuffled_password

def clear():
    first_name_entry.delete(0, END)
    middle_name_entry.delete(0, END)
    last_name_entry.delete(0,END)
    email_address_entry.delete(0,END) 
    contact_no_entry.delete(0,END)
    age_entry.delete(0,END)
    uploaded_label.grid_forget()
    role_combo_box.set("Select")
    age_entry.config(state=NORMAL)
    age_entry.delete(0, END)
    age_entry.config(state=DISABLED)

def now_date():
    current_date = datetime.now()
    eighteen_years_ago = current_date - timedelta(days=365.25 * 18)
    # eighteen_years_ago_date = eighteen_years_ago.date()
    return eighteen_years_ago

def update_age(event):
    # selected_date = birth_date.get_date()
    # birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    selected_date = datetime.strptime(str(birth_date.get_date()), '%Y-%m-%d')

    today = datetime.today()
    age = today.year - selected_date.year - ((today.month, today.day) < (selected_date.month, selected_date.day))

    age_entry.config(state=NORMAL)
    age_entry.delete(0, END)
    age_entry.insert(0, str(age))
    age_entry.config(state=DISABLED)

def submit_employee_details():
    role_combo_box.config(state=NORMAL)
    if first_name_entry.get()=="" or middle_name_entry.get()=="" or last_name_entry.get()=="" or contact_no_entry.get()=="" or email_address_entry.get()=="" or role_combo_box.get()=="Select":
        messagebox.showerror(title="Error", message="Please fill all the fields")
    # print(birth_date.get_date())     
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
            query = 'create table user(username VARCHAR(50) NOT NULL PRIMARY KEY,password VARCHAR(50) NOT NULL,role VARCHAR(25) NOT NULL, first_name VARCHAR(255) NOT NULL ,middle_name VARCHAR(255) NOT NULL,last_name VARCHAR(225) NOT NULL,email_address VARCHAR(255) NOT NULL,contact_no VARCHAR(10),birth_date DATE,date_of_joining DATE,image_data LONGBLOB)'
            mycursor.execute(query)
        except:
            query='use warehouse'
            mycursor.execute(query)
        # file_path = filedialog.askopenfilename()
        if file_path:
        # Read the image file as binary data
            with open(file_path, 'rb') as file:
                image_data = file.read()
        else:
            messagebox.showerror("Error", "Please Upload Photo.")
            return

        query="insert into user (username,password,role, first_name,middle_name,last_name,email_address,contact_no,birth_date,date_of_joining,image_data) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(query,(generate_username(),generate_password(),role_combo_box.get(),first_name_entry.get(),middle_name_entry.get(),last_name_entry.get(),email_address_entry.get(),contact_no_entry.get(),birth_date.get_date(),join_date.get_date(),image_data))
        con.commit()
        con.close()
        messagebox.showinfo('Success','Registration is Successful')
        clear()  
          
def upload_photo():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:

        uploaded_label.grid(row=9,column=2)
        image = Image.open(file_path)
        image.thumbnail((50, 50))  
        photo = ImageTk.PhotoImage(image)
        uploaded_label.config(image=photo)
        uploaded_label.image = photo

def going_to_add_frame():
    search_attributes_frame.place_forget()
    search_tree_scroll_frame.place_forget()
    add_frame.place(relx=0,rely=0,relheight=1,relwidth=1)

def search_frame():
    add_frame.place_forget()
    search_attributes_frame.place(relx=0,rely=0,relwidth=1,relheight=0.25)
    search_tree_scroll_frame.place(relx=0,rely=0.25,relwidth=1,relheight=0.75)

admin_page=Tk()
admin_page.title("WAREHOUSE")
admin_page.geometry("1200x675")


# left frame
admin_page_left_frame=Frame(admin_page)
admin_page_left_frame.place(relx=0,rely=0,relwidth=0.20,relheight=1)

admin_page_left_frame.rowconfigure((0,1,2,3,4),weight=1, uniform = 'a')
admin_page_left_frame.columnconfigure(0,weight=1)

admin_page_left_add_button=Button(admin_page_left_frame,text="ADD",command=going_to_add_frame)
admin_page_left_add_button.grid(row=0,column=0,sticky='nsew',padx=20,pady=25)

admin_page_search_button=Button(admin_page_left_frame,text="SEARCH",command=search_frame)
admin_page_search_button.grid(row=1,column=0,sticky='nsew',padx=20,pady=25)

# right frame

admin_page_right_frame=Frame(admin_page)
admin_page_right_frame.place(relx=0.20,rely=0,relwidth=0.80,relheight=1)

# add frame
add_frame=Frame(admin_page_right_frame)

personal_details_Lframe=LabelFrame(add_frame,text= "Personal Details")
personal_details_Lframe.pack(expand = True, fill=BOTH)

role_selection_label=Label(personal_details_Lframe,text="ROLE")
role_selection_label.grid(row=0,column=0)
role_combo_var=StringVar()
role_combo_box =ttk.Combobox(personal_details_Lframe,textvariable=role_combo_var,state="readonly")
role_combo_box['values'] = ('Admin', 'Employee')
role_combo_box.grid(row=0,column=1)
role_combo_box.set("Select")

first_name_label=Label(personal_details_Lframe,text="FIRST NAME")
first_name_label.grid(row=1,column=0)
first_name_entry=Entry(personal_details_Lframe)
first_name_entry.grid(row=1,column=1)

middle_name_label=Label(personal_details_Lframe,text="MIDDLE NAME")
middle_name_label.grid(row=2,column=0)
middle_name_entry=Entry(personal_details_Lframe)
middle_name_entry.grid(row=2,column=1)

last_name_label=Label(personal_details_Lframe,text="LAST NAME")
last_name_label.grid(row=3,column=0)
last_name_entry=Entry(personal_details_Lframe)
last_name_entry.grid(row=3,column=1)

date_of_birth_label=Label(personal_details_Lframe,text="Date of Birth")
date_of_birth_label.grid(row=4,column=0)
birth_date = DateEntry(personal_details_Lframe,state='readonly')
birth_date.grid(row=4,column=1)

eighteen_years_ago = now_date()
birth_date.set_date(eighteen_years_ago.date())
birth_date.configure(maxdate=eighteen_years_ago.date())
birth_date.bind("<<DateEntrySelected>>", update_age)

age_label=Label(personal_details_Lframe,text="AGE")
age_label.grid(row=5,column=0)
age_entry=Entry(personal_details_Lframe, state='readonly')
age_entry.grid(row=5,column=1)

contact_no_label=Label(personal_details_Lframe,text="CONTACT NO")
contact_no_label.grid(row=6,column=0)
contact_no_entry=Entry(personal_details_Lframe)
contact_no_entry.grid(row=6,column=1)

email_address_label=Label(personal_details_Lframe,text="EMAIL")
email_address_label.grid(row=7,column=0)
email_address_entry=Entry(personal_details_Lframe)
email_address_entry.grid(row=7,column=1)

    
date_of_joining_label=Label(personal_details_Lframe,text="Date of Joining")
date_of_joining_label.grid(row=8,column=0)
join_date = DateEntry(personal_details_Lframe,state='readonly')
join_date.grid(row=8,column=1)

photo_label=Label(personal_details_Lframe,text="PASSPORT PHOTO")
photo_label.grid(row=9, column=0)
upload_button=Button(personal_details_Lframe,text="UPLOAD",command=upload_photo)
upload_button.grid(row=9,column=1)

uploaded_label = Label(personal_details_Lframe)

submit_button=Button(personal_details_Lframe,text="SUBMIT",command=submit_employee_details)
submit_button.grid(row=10,columnspan=2)

first_name_entry.bind("<Return>",lambda event:middle_name_entry.focus())
middle_name_entry.bind("<Return>",lambda event:last_name_entry.focus())
contact_no_entry.bind("<Return>",lambda event:email_address_entry.focus())

# search frame
# search_frame=Frame(admin_page_right_frame)

search_attributes_frame = Frame(admin_page_right_frame)

search_attributes_frame.columnconfigure((0,1,2,3),weight=1,uniform = 'a')
search_attributes_frame.rowconfigure((0,1),weight=1,uniform='a')
search_attributes_frame.rowconfigure(2,weight=2,uniform='a')

style = ttk.Style()
style.theme_create("custom_style", parent="alt", settings={
    "TCombobox": {
        "configure": {
            "background": "white",
            "foreground": "#163246",
            "selectbackground": "white",
            "selectforeground": "#163246",
            "arrowcolor": "#163246",
        },
        "map": {
            "background": [("active", "white")],
            "foreground": [("active", "#163246")],
        },
    },
})

style.theme_use("custom_style")


employee_role_label=Label(search_attributes_frame,text="ROLE")
employee_role_label.grid(row=0,column=0,sticky='e')
search_role_combo_var=StringVar()
search_role_combo_box =ttk.Combobox(search_attributes_frame,textvariable=search_role_combo_var,state="readonly", style="TCombobox",font=('Times New Roman',15))
search_role_combo_box['values'] = ('Admin', 'Employee')
search_role_combo_box.grid(row=0,column=1,sticky='nsew',padx=10,pady=5)
search_role_combo_box.set("Select")

employee_username_label=Label(search_attributes_frame,text="USERNAME")
employee_username_label.grid(row=0,column=2,sticky='e')
employee_username_entry=Entry(search_attributes_frame)
employee_username_entry.grid(row=0,column=3)

employee_year_label=Label(search_attributes_frame,text="YEAR")
employee_year_label.grid(row=1,column=0,sticky='e')
employee_year_entry=Entry(search_attributes_frame)
employee_year_entry.grid(row=1,column=1)   

employee_month_label=Label(search_attributes_frame,text="MONTH")
employee_month_label.grid(row=1,column=2,sticky='e')
employee_month_entry=Entry(search_attributes_frame)
employee_month_entry.grid(row=1,column=3) 

employee_reset_button=Button(search_attributes_frame,text="RESET")
employee_reset_button.grid(row=2,column=0)

employee_select_button=Button(search_attributes_frame,text="SEARCH")
employee_select_button.grid(row=2,column=1,columnspan=2)

employee_select_button=Button(search_attributes_frame,text="UPDATE")
employee_select_button.grid(row=2,column=3)

search_tree_scroll_frame = Frame(admin_page_right_frame)


tree = ttk.Treeview(search_tree_scroll_frame, columns=(1,2,3,4,5,6,7,8), show="headings",height=100)
tree.heading(1, text="ROLE")
tree.heading(2, text="USERNAME")
tree.heading(3, text="FIRST_NAME")
tree.heading(4, text="LAST_NAME")
tree.heading(5, text="EMAIL_ADDRESS")
tree.heading(6, text="CONTACT_NO")
tree.heading(7, text="BIRTH_DATE")
tree.heading(8, text="JOINING_DATE")

tree_y_scroll = Scrollbar(search_tree_scroll_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_y_scroll.set)
tree_y_scroll.pack(side='right',fill=Y)

tree_x_scroll = Scrollbar(search_tree_scroll_frame, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=tree_x_scroll.set)
tree_x_scroll.pack(side='bottom',fill=X)

tree.pack()
# search_frame.columnconfigure(0, weight=1)


admin_page.mainloop()