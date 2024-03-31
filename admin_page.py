from tkinter import *
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import filedialog
from datetime import datetime, timedelta
import secrets
import string
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import ttkthemes
import io

def generate_qrcode(data_tuple):

    # Data to be stored in the QR code
    # data_tuple = ("John Doe", "john.doe@example.com", "123456789")

    # Combine the data into a single string
    combined_data = "\n".join(data_tuple)

    # Create a QRCode instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QRCode instance
    qr.add_data(combined_data)
    qr.make(fit=True)

    # Create an image from the QRCode instance
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create a drawing object
    draw = ImageDraw.Draw(qr_img)

    # Specify the path to your custom font file
    font_path = "font/Roboto-Regular.ttf"  # Adjust this path accordingly

    # Load the custom font
    font = ImageFont.truetype(font_path, size=25)

    # Get the text to be added (in this case, the name from the data list)
    name_tup = (data_tuple[0][0],data_tuple[1],data_tuple[3])
    name = '_'.join(name_tup)  # Replace spaces with underscores for a clean filename

    # Calculate the position for top-center
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # right - left
    image_width, _ = qr_img.size
    text_position = ((image_width - text_width) / 2, 10)

    # Add the name to the image
    draw.text(text_position, name, font=font, fill="black")

    return qr_img

    # Save the image with the added name
    # filename = f"qrcode_{name}.png"
    # qr_img.save(filename)

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
    uploaded_label.grid_forget()
    role_combo_box.set("Select")
    age_entry.config(state=NORMAL)
    age_entry.delete(0, END)
    age_entry.config(state=DISABLED)
    eighteen_years_ago = now_date()
    birth_date.set_date(eighteen_years_ago.date())
    try:
        join_date.set_date(today.date())
    except:
        pass

def now_date():
    current_date = datetime.now()
    eighteen_years_ago = current_date - timedelta(days=365.25 * 18)
    # eighteen_years_ago_date = eighteen_years_ago.date()
    return eighteen_years_ago

def update_age(event):
    global today
    # selected_date = birth_date.get_date()
    # birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    selected_date = datetime.strptime(str(birth_date.get_date()), '%Y-%m-%d')

    today = datetime.today()
    age = today.year - selected_date.year - ((today.month, today.day) < (selected_date.month, selected_date.day))

    age_entry.configure(state=NORMAL)
    age_entry.delete(0, END)
    age_entry.insert(0, str(age))
    age_entry.configure(state=DISABLED)

def confirm_dialog():
    def delete_info():
        clear()
        dialog.destroy()

    def add_info():
        bool = submit_employee_details(user_entry.get())
        if bool == True:
            dialog.destroy()
        
    if first_name_entry.get()=="" or middle_name_entry.get()=="" or last_name_entry.get()=="" or contact_no_entry.get()=="" or email_address_entry.get()=="" or role_combo_box.get()=="Select":
        messagebox.showerror(title="Error", message="Please fill all the fields")
    else:
        dialog = Toplevel()
        dialog.grab_set()
        dialog.title('Confirmation')
        dialog.geometry('400x400')
        dialog.resizable(0,0)
        dialog.config(background='#e9e3d5')

        dialog.rowconfigure((0,2), weight = 2, uniform = 'a')
        dialog.rowconfigure((1,3,4), weight = 1, uniform = 'a')
        dialog.columnconfigure((0,1), weight = 1, uniform = 'a')

        photo_lbl = Label(dialog)
        photo_lbl.grid(row=0,column=0, columnspan=2)
        image = Image.open(file_path)
        image.thumbnail((125, 125))  
        photo = ImageTk.PhotoImage(image)
        photo_lbl.config(image=photo)
        photo_lbl.image = photo

        user_label = Label(dialog, text = "USERNAME",
                           bg ="#e9e3d5",bd=0,fg="#021530",
                           font=("Times New Roman",20,"bold"))
        user_label.grid(row=1, column = 0)
        user_entry = CTkEntry(dialog,width=185,height=35,
                              corner_radius=10.5,border_color='#373737',
                              fg_color='#e9e3d5',text_color='#373737',
                              font=("Times New Roman",14,"bold"))
        user_entry.grid(row=1, column= 1)
        user_entry.insert(0,email_address_entry.get())
        # password_entry = CTkEntry(main_frame,width=185,height=35,corner_radius=10.5,border_color='#373737',show='*',fg_color='#e9e3d5',text_color='#373737',font=("Times New Roman",14,"bold"))

        qr_lbl = Label(dialog)
        qr_lbl.grid(row=2,column=0, columnspan=2)
        data_tuple = (role_combo_box.get(),first_name_entry.get(),middle_name_entry.get(),last_name_entry.get(),str(birth_date.get_date()),str(join_date.get_date()))
        qr_img = generate_qrcode(data_tuple)
        qr_img.thumbnail((125, 125))
        qr_photo = ImageTk.PhotoImage(qr_img)
        qr_lbl.config(image=qr_photo)
        qr_lbl.image = qr_photo

        question_label = Label(dialog, text = 'Do you want to add the member in the warehouse?',
                               bg ="#e9e3d5",bd=0,font=("Times New Roman",12,"bold"),fg="#021530")
        question_label.grid(row=3,column=0, columnspan= 2)

        yes_button = CTkButton(dialog, text = "YES",command=add_info,width=120,height=30,
                               corner_radius=12,font=("Times New Roman",25,"bold"),
                               fg_color='#373737',text_color='#e9e3d5',hover_color='white')
        yes_button.grid(row=4,column=0)

        no_button = CTkButton(dialog,text = "NO", command=delete_info,width=120,height=30,
                              corner_radius=12,font=("Times New Roman",25,"bold"),
                              fg_color='#373737',text_color='#e9e3d5',hover_color='white')
        no_button.grid(row=4,column=1) 

        dialog.mainloop()

def submit_employee_details(username):
    role_combo_box.config(state=NORMAL)

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
        create_table_query = 'create table user(username VARCHAR(50) NOT NULL PRIMARY KEY,password VARCHAR(50) NOT NULL,role VARCHAR(25) NOT NULL, first_name VARCHAR(255) NOT NULL ,middle_name VARCHAR(255) NOT NULL,last_name VARCHAR(225) NOT NULL,email_address VARCHAR(255) NOT NULL,contact_no VARCHAR(10),birth_date DATE,date_of_joining DATE,image_data LONGBLOB)'
        mycursor.execute(create_table_query)
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
    
    check_user_query = 'select * from user where username=%s'
    mycursor.execute(check_user_query,username)
    tup = mycursor.fetchone()
    if tup != None:
        messagebox.showerror('Error','Username Already Exist. Please Use Other Username.')
        return False
    else:
        insert_user_query="insert into user (username,password,role, first_name,middle_name,last_name,email_address,contact_no,birth_date,date_of_joining,image_data) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(insert_user_query,(username,generate_password(),role_combo_box.get(),first_name_entry.get(),middle_name_entry.get(),last_name_entry.get(),email_address_entry.get(),contact_no_entry.get(),birth_date.get_date(),join_date.get_date(),image_data))
        con.commit()
        con.close()
        messagebox.showinfo('Success','Registration is Successful')
        save_qr()
        clear()
        return True

def save_qr():
    data_tuple = (role_combo_box.get(),first_name_entry.get(),middle_name_entry.get(),last_name_entry.get(),str(birth_date.get_date()),str(join_date.get_date()))
    qr_img = generate_qrcode(data_tuple)
    
    name_tup = data_tuple[0:4]
    name = '_'.join(name_tup)  # Replace spaces with underscores for a clean filename

    # Specify the folder to save the image
    save_folder = "qr"

    # Create the folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)

    # Save the image with the added name
    filename = f"qrcode_{name}.png"

    # Save the image in the specified folder with a custom name
    save_path = os.path.join(save_folder, filename)
    qr_img.save(save_path)

def upload_photo():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:

        uploaded_label.grid(row=1,column=0)
        image = Image.open(file_path)
        image.thumbnail((150, 150))  
        # print(image)
        photo = ImageTk.PhotoImage(image)
        uploaded_label.config(image=photo)
        uploaded_label.image = photo

def going_to_add_frame():
    search_frame.place_forget()
    add_frame.place(relx=0.0,rely=0.05,relwidth=0.95,relheight=0.9)

def search_frame():
    add_frame.place_forget()
    search_frame.place(relx=0.0,rely=0.05,relwidth=0.95,relheight=0.9)
    retrieve_data()

def retrieve_data():
    # Iterate over all items in the treeview and delete them
    for item in tree.get_children():
        tree.delete(item)
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
        create_table_query = 'create table user(username VARCHAR(50) NOT NULL PRIMARY KEY,password VARCHAR(50) NOT NULL,role VARCHAR(25) NOT NULL, first_name VARCHAR(255) NOT NULL ,middle_name VARCHAR(255) NOT NULL,last_name VARCHAR(225) NOT NULL,email_address VARCHAR(255) NOT NULL,contact_no VARCHAR(10),birth_date DATE,date_of_joining DATE,image_data LONGBLOB)'
        mycursor.execute(create_table_query)
    except:
        query='use warehouse'
        mycursor.execute(query)

    all_data = "select * from user"
    mycursor.execute(all_data)
    fetch_all = mycursor.fetchall()
    for i in fetch_all:
        tree.insert("", "end", values=(i[2], i[0], i[3], i[5],i[6],i[7],i[8],i[9]))

    data = [(tree.set(child, 1),tree.set(child, 3), child) for child in tree.get_children('')]
    data.sort(key=lambda x: (x[0], x[1]))
    for index, (role,fname, child) in enumerate(data):
        tree.move(child, '', index)


admin_page=Tk()
admin_page.title("WAREHOUSE")
admin_page.geometry("1200x675+0+0")
admin_page.title("admin_page")
admin_page.resizable(0,0)
admin_page.iconbitmap('image\\page_icon.ico')

# left frame
admin_page_left_frame=Frame(admin_page,bg ="#E9E3D5")
admin_page_left_frame.place(relx=0,rely=0,relwidth=0.20,relheight=1)

admin_page_left_frame.columnconfigure(0,weight=1,uniform="A")

admin_page_left_add_button=CTkButton(admin_page_left_frame,text="ADD",command=going_to_add_frame,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
admin_page_left_add_button.grid(row=0,column=0,pady=(50,10))


admin_page_search_button=CTkButton(admin_page_left_frame,text="SEARCH",command=search_frame,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
admin_page_search_button.grid(row=1,column=0,pady=10)

# right frame

admin_page_right_frame=Frame(admin_page,bg ="#E9E3D5",borderwidth=5)
admin_page_right_frame.place(relx=0.20,rely=0,relwidth=0.80,relheight=1)

# add frame
add_frame=Frame(admin_page_right_frame,borderwidth=5,relief='groove',bg="white")
add_frame.columnconfigure((0,1),weight=1,uniform='a')

personal_details_Lframe=LabelFrame(add_frame,text= "Personal Details",font=("Poppins",12,"bold"),bg="white")
personal_details_Lframe.pack(expand = True, fill=BOTH,padx=25,pady=25)
personal_details_Lframe.columnconfigure((0,1),weight=1,uniform='a')
personal_details_Lframe.rowconfigure((0,1,2,3,4,4,6),weight=1,uniform='a')



role_selection_labelFrame=LabelFrame(personal_details_Lframe,text="ROLE",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
role_selection_labelFrame.grid(row=0,column=0)

role_combo_var=StringVar()
role_combo_box =CTkComboBox(role_selection_labelFrame,variable=role_combo_var,
                                width=175,height=35,
								corner_radius=15,
								fg_color='#e9e3d5',text_color='#373737',
								border_color='#373737',
								button_color='#373737',
								font=("Times New Roman",12,"bold"),
								button_hover_color='#e9e3d5',
								dropdown_fg_color='white',
								dropdown_hover_color='#e9e3d5',
								dropdown_font=("Times New Roman",15,"bold"),
								dropdown_text_color='#373737',
								justify='center',
								state='readonly',
								border_width=3)
role_combo_box['values'] = ('Admin', 'Employee')
role_combo_box.grid(row=0,column=1,padx=5,pady=8)
role_combo_box.set("Select")

first_name_labelFrame=LabelFrame(personal_details_Lframe,text="FIRST NAME",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
first_name_labelFrame.grid(row=1,column=0)
first_name_entry=CTkEntry(first_name_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='#E9E3D5',text_color='#373737',font=("Times New Roman",14,"bold"))
first_name_entry.grid(row=1,column=1,padx=5,pady=8)

middle_name_labelFrame=LabelFrame(personal_details_Lframe,text="MIDDLE NAME",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
middle_name_labelFrame.grid(row=2,column=0)
middle_name_entry=CTkEntry(middle_name_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='#E9E3D5',text_color='#373737',font=("Times New Roman",14,"bold"))
middle_name_entry.grid(row=2,column=1,padx=5,pady=8)

last_name_labelFrame=LabelFrame(personal_details_Lframe,text="LAST NAME",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
last_name_labelFrame.grid(row=3,column=0)
last_name_entry=CTkEntry(last_name_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='#E9E3D5',text_color='#373737',font=("Times New Roman",14,"bold"))
last_name_entry.grid(row=3,column=1,padx=5,pady=8)

date_of_birth_labelFrame=LabelFrame(personal_details_Lframe,text="DATE OF BIRTH",font=("Times New Roman",15,"bold"),bg="white",fg="#021530",width=40)
date_of_birth_labelFrame.grid(row=4,column=0)
birth_date = DateEntry(date_of_birth_labelFrame,state='readonly', date_pattern='yyyy-mm-dd',width=26,height=70)
birth_date.grid(row=4,column=1,padx=5,pady=8)

eighteen_years_ago = now_date()
birth_date.set_date(eighteen_years_ago.date())
birth_date.configure(maxdate=eighteen_years_ago.date())
birth_date.bind("<<DateEntrySelected>>", update_age)

age_labelFrame=LabelFrame(personal_details_Lframe,text="AGE",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
age_labelFrame.grid(row=5,column=0)
age_entry=CTkEntry(age_labelFrame,state='readonly',width=175,height=35,corner_radius=10,border_color='#373737',fg_color='#E9E3D5',text_color='#373737',font=("Times New Roman",14,"bold"))
age_entry.grid(row=5,column=1,padx=5,pady=8)

contact_no_labelFrame=LabelFrame(personal_details_Lframe,text="CONTACT NO",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
contact_no_labelFrame.grid(row=0,column=1)
contact_no_entry=CTkEntry(contact_no_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='#E9E3D5',text_color='#373737',font=("Times New Roman",14,"bold"))
contact_no_entry.grid(row=6,column=1,padx=5,pady=8)

email_address_labelFrame=LabelFrame(personal_details_Lframe,text="EMAIL",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
email_address_labelFrame.grid(row=1,column=1)
email_address_entry=CTkEntry(email_address_labelFrame,width=175,height=35,corner_radius=10,border_color='#373737',fg_color='#E9E3D5',text_color='#373737',font=("Times New Roman",14,"bold"))
email_address_entry.grid(row=7,column=1,padx=5,pady=8)
    
date_of_joining_labelFrame=LabelFrame(personal_details_Lframe,text="DATE OF JOINING",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
date_of_joining_labelFrame.grid(row=2,column=1)
join_date = DateEntry(date_of_joining_labelFrame,state='readonly', date_pattern='yyyy-mm-dd',width=26,height=70)
join_date.grid(row=8,column=1,padx=5,pady=8)

photo_labelFrame=LabelFrame(personal_details_Lframe,text="PASSPORT PHOTO",font=("Times New Roman",15,"bold"),bg="white",fg="black",width=40)
photo_labelFrame.grid(row=3, column=1,rowspan=3,sticky="n")
photo_labelFrame.columnconfigure((0),weight=1,uniform='a')
upload_button=CTkButton(photo_labelFrame,text="UPLOAD",command=upload_photo,width=100,height=20,corner_radius=8,font=("Times New Roman",20,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
upload_button.grid(row=0,column=0,padx=5,pady=8)

uploaded_label = Label(photo_labelFrame)


submit_button=CTkButton(personal_details_Lframe,text="SUBMIT",command=confirm_dialog,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
submit_button.grid(row=6,column=0,columnspan=2)

first_name_entry.bind("<Return>",lambda event:middle_name_entry.focus())
middle_name_entry.bind("<Return>",lambda event:last_name_entry.focus())
contact_no_entry.bind("<Return>",lambda event:email_address_entry.focus())

#---------------------------------------------------------------------------------------------------
# search frame
search_frame=Frame(admin_page_right_frame,borderwidth=5,relief='groove',bg="white")

search_attributes_frame = Frame(search_frame,bg="white")
search_attributes_frame.place(relx=0,rely=0,relwidth=1,relheight=0.15)
search_attributes_frame.rowconfigure(0,weight=1)
search_attributes_frame.columnconfigure((0,1,2,3,4,5),weight=1)

employee_role_label=CTkLabel(search_attributes_frame,text="ROLE",fg_color="#e9e3d5",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
employee_role_label.grid(row=0,column=0,sticky='e')
search_role_combo_var=StringVar(value="SELECT")
search_role_combo_box=CTkComboBox(search_attributes_frame,variable=search_role_combo_var,
                                  values=["ADMIN", "EMPLOYEE","NONE"],width=140,height=40,
								   corner_radius=15,
								   fg_color='#e9e3d5',text_color='#373737',
								   border_color='#373737',
								   button_color='#373737',
								   font=("Times New Roman",12,"bold"),
								   button_hover_color='#e9e3d5',
								   dropdown_fg_color='white',
								   dropdown_hover_color='#e9e3d5',
								   dropdown_font=("Times New Roman",15,"bold"),
								   dropdown_text_color='#373737',
								   justify='center',
								   state='readonly',
								   border_width=3)

search_role_combo_box.grid(row=0,column=1,padx=10,pady=5)
search_role_combo_box.set("SELECT")

employee_username_label=CTkLabel(search_attributes_frame,text="USERNAME",fg_color="#e9e3d5",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
employee_username_label.grid(row=0,column=2)
employee_username_entry=CTkEntry(search_attributes_frame,width=185,height=35,corner_radius=10.5,border_color='#373737',fg_color='#e9e3d5',text_color='#373737',font=("Times New Roman",14,"bold"))
employee_username_entry.grid(row=0,column=3)

employee_year_label=CTkLabel(search_attributes_frame,text="YEAR",fg_color="#e9e3d5",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
employee_year_label.grid(row=0,column=4)
employee_year_entry=CTkEntry(search_attributes_frame,width=185,height=35,corner_radius=10.5,border_color='#373737',fg_color='#e9e3d5',text_color='#373737',font=("Times New Roman",14,"bold"))
employee_year_entry.grid(row=0,column=5)   

search_tree_scroll_frame = Frame(search_frame,bg="white")
search_tree_scroll_frame.place(relx=0,rely=0.15,relwidth=1,relheight=0.7)


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

style=ttkthemes.ThemedStyle(tree)
# print(style.get_themes)
style.theme_use('clam')
style.configure('Treeview',font=("Times New Roman",10),foreground='black',background="white")
style.configure('Treeview.Heading',font=("Times New Roman",10,"bold"),foreground='#e9e3d5',background='#373737')
style.map("Treeview", background= [('selected','#e9e3d5')], foreground= [('selected','#373737')])
style.map("Treeview.Heading", background= [('selected','#373737')], foreground= [('selected','#e9e3d5')])

search_button_frame = Frame(search_frame,bg="white")
search_button_frame.place(relx=0,rely=0.85,relheight=0.15,relwidth=1)
search_button_frame.rowconfigure(0,weight=1)
search_button_frame.columnconfigure((0,1,2),weight=1)

def reset_user():
    search_role_combo_box.set("SELECT")
    employee_year_entry.delete(0,END)
    employee_username_entry.delete(0,END)
    retrieve_data()

employee_reset_button=CTkButton(search_button_frame,command=reset_user,text="RESET",width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
employee_reset_button.grid(row=0,column=0)

def search_user():
    flag=0
    string=""
    lst=[]
    if (search_role_combo_box.get()=="SELECT" or search_role_combo_box.get()=="NONE") and employee_username_entry.get()=="" and employee_year_entry.get()=="":
        messagebox.showerror('Error','Fill Something to search.')
    else:
        try:
            con = pymysql.connect(host='localhost',user='root',password='root',database="warehouse")
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Database Connectivity Issue, Try Again')
            return 
        if search_role_combo_box.get()!="NONE":
            string="role=%s"
            lst.append(search_role_combo_box.get())
            flag=1
        if employee_username_entry.get()!="":
            lst.append(employee_username_entry.get())
            if flag==1:
                string+=" and username=%s"
            else:
                string+="username=%s" 
            flag=2
        if employee_year_entry.get()!="":
            lst.append(employee_year_entry.get())
            if flag==2 or flag==1:
                string+=" and YEAR(date_of_joining)=%s"
            else:
                string+="YEAR(date_of_joining)=%s" 
            flag=0
        query="SELECT * FROM user WHERE " + string
        # print(query)
        # print(tuple(lst))
        mycursor.execute(query,tuple(lst))
        fetch_row = mycursor.fetchall()
        for item in tree.get_children():
            tree.delete(item)
        for i in fetch_row:
            tree.insert("", "end", values=(i[2], i[0], i[3], i[5],i[6],i[7],i[8],i[9]))

employee_search_button=CTkButton(search_button_frame,text="SEARCH",command=search_user,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
employee_search_button.grid(row=0,column=1)

def view_users():

    # Check if any item is selected in the treeview
    if not tree.selection():
        messagebox.showerror('Error', 'Please select an Admin/Employee from the list.')
        return
    
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, 'values')

    try:
        con = pymysql.connect(host='localhost', user='root', password='root',database="warehouse")
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error', 'Connection is not established try again.')
        return
    
    query="select * from user where username=%s"
    mycursor.execute(query,(values[1]))
    fetch_data=mycursor.fetchone()

    # Convert binary data to image
    image = Image.open(io.BytesIO(fetch_data[10]))

    # Resize image if necessary
    image = image.resize((85, 85))

    # Convert image to PhotoImage
    photo = ImageTk.PhotoImage(image)

    # Update label with image
    # label.config(image=photo)
    # label.image = photo


    window = Toplevel()
    window.title("User Information")
    window.geometry("480x500")
    window.grab_set()
    window.config(bg='#e9e3d5')

    photo_lbl=Label(window)
    photo_lbl.config(image=photo)
    photo_lbl.image = photo
    photo_lbl.grid(row=0,column=0,columnspan=2)

    emp_role_label=CTkLabel(window,text="ROLE",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_role_label.grid(row=1,column=0,sticky='nsew',pady=5,padx=20)
    emp_role_entry=Label(window, text=values[0],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid"
                          )
    emp_role_entry.grid(row=1,column=1,sticky='ew')

    emp_username_label=CTkLabel(window,text="USERNAME",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_username_label.grid(row=2,column=0,sticky='nsew',pady=5,padx=20)
    emp_username_entry=Label(window, text=values[1],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_username_entry.grid(row=2,column=1,sticky='ew')

    emp_fname_label=CTkLabel(window,text="FIRST_NAME",fg_color="#373737",font=("Times New Roman",20,"bold"),text_color="#e9e3d5",corner_radius=10)
    emp_fname_label=CTkLabel(window,text="FIRST_NAME",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_fname_label.grid(row=3,column=0,sticky='nsew',pady=5,padx=20)
    emp_fname_entry=Label(window, text=values[2],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_fname_entry.grid(row=3,column=1,sticky='ew')

    emp_Mname_label=CTkLabel(window,text="MIDDLE_NAME",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_Mname_label.grid(row=4,column=0,sticky='nsew',pady=5,padx=20)
    emp_Mname_entry=Label(window,text=fetch_data[4],
                          background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_Mname_entry.grid(row=4,column=1,sticky='ew')

    emp_lname_label=CTkLabel(window,text="LAST_NAME",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_lname_label.grid(row=5,column=0,sticky='nsew',pady=5,padx=20)
    emp_lname_entry=Label(window, text=values[3],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_lname_entry.grid(row=5,column=1,sticky='ew')

    emp_email_address_label=CTkLabel(window,text="EMAIL",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_email_address_label.grid(row=6,column=0,sticky='nsew',pady=5,padx=20)
    emp_email_address_entry=Label(window, text=values[4],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_email_address_entry.grid(row=6,column=1,sticky='ew')

    emp_contact_no_label=CTkLabel(window,text="PHONE_NO",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_contact_no_label.grid(row=7,column=0,sticky='nsew',pady=5,padx=20)
    emp_contact_no_entry=Label(window, text=values[5],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_contact_no_entry.grid(row=7,column=1,sticky='ew')

    emp_birth_date_label=CTkLabel(window,text="BIRTH_DATE",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_birth_date_label.grid(row=8,column=0,sticky='nsew',pady=5,padx=20)
    emp_birth_date_entry=Label(window, text=values[6],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_birth_date_entry.grid(row=8,column=1,sticky='ew')

    emp_join_date_label=CTkLabel(window,text="JOINING_DATE",fg_color="white",font=("Times New Roman",20,"bold"),text_color="#373737",corner_radius=10)
    emp_join_date_label.grid(row=9,column=0,sticky='nsew',pady=(5,20),padx=20)
    emp_join_date_entry=Label(window, text=values[7],background="white",
                          font=("Times New Roman",15,"bold"),
                          fg="#373737",bd=2,relief="solid")
    emp_join_date_entry.grid(row=9,column=1,sticky='ew',pady=(5,20))


    def update_emp_admin():
        emp_fname_entry.grid_forget()
        emp_Mname_entry.grid_forget()
        emp_lname_entry.grid_forget()
        emp_email_address_entry.grid_forget()
        emp_contact_no_entry.grid_forget()
        emp_birth_date_entry.grid_forget()
        emp_join_date_entry.grid_forget()


        emp_fname_entr=CTkEntry(window,width=150,height=30,corner_radius=10.5,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
        emp_fname_entr.grid(row=3,column=1,sticky='ew')
        emp_fname_entr.insert(0,values[2])

        emp_Mname_entr=CTkEntry(window,width=150,height=30,corner_radius=10.5,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
        emp_Mname_entr.grid(row=4,column=1,sticky='ew')
        emp_Mname_entr.insert(0,fetch_data[4])

        emp_lname_entr=CTkEntry(window,width=150,height=30,corner_radius=10.5,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
        emp_lname_entr.grid(row=5,column=1,sticky='ew')
        emp_lname_entr.insert(0,values[3])

        emp_email_address_entr=CTkEntry(window,width=150,height=30,corner_radius=10.5,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
        emp_email_address_entr.grid(row=6,column=1,sticky='ew')
        emp_email_address_entr.insert(0,values[4])

        emp_contact_no_entr=CTkEntry(window,width=150,height=30,corner_radius=10.5,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
        emp_contact_no_entr.grid(row=7,column=1,sticky='ew')
        emp_contact_no_entr.insert(0,values[5])

        emp_birth_date_entr=CTkEntry(window,width=150,height=30,corner_radius=10.5,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
        emp_birth_date_entr.grid(row=8,column=1,sticky='ew')
        emp_birth_date_entr.insert(0,values[6])

        emp_join_date_entr=CTkEntry(window,width=150,height=30,corner_radius=10.5,border_color='#373737',fg_color='white',text_color='#373737',font=("Times New Roman",14,"bold"))
        emp_join_date_entr.grid(row=9,column=1,sticky='ew',pady=(5,20))
        emp_join_date_entr.insert(0,values[7])

        def cancel_emp_admin():
            emp_submit_button.grid_forget()
            emp_cancel_button.grid_forget()
            emp_fname_entr.grid_forget()
            emp_Mname_entr.grid_forget()
            emp_lname_entr.grid_forget()
            emp_email_address_entr.grid_forget()
            emp_contact_no_entr.grid_forget()
            emp_birth_date_entr.grid_forget()
            emp_join_date_entr.grid_forget()
            emp_join_date_entry.grid(row=9,column=1,sticky='ew',pady=(5,20))
            emp_birth_date_entry.grid(row=8,column=1,sticky='ew')
            emp_contact_no_entry.grid(row=7,column=1,sticky='ew')
            emp_email_address_entry.grid(row=6,column=1,sticky='ew')
            emp_lname_entry.grid(row=5,column=1,sticky='ew')
            emp_Mname_entry.grid(row=4,column=1,sticky='ew')
            emp_fname_entry.grid(row=3,column=1,sticky='ew')

        emp_cancel_button=CTkButton(window,text="CANCEL",
                                    command=cancel_emp_admin,
                                    width=150,
                                    height=40,
                                    corner_radius=12,
                                    font=("Times New Roman",25,"bold"),
                                    fg_color='#373737',
                                    text_color='#e9e3d5',
                                    hover_color='black')
        emp_cancel_button.grid(row=10,column=0)

        def submit_emp_admin():
            update_query = "UPDATE user SET first_name = %s, middle_name = %s, last_name = %s, email_address = %s, contact_no = %s, birth_date = %s, date_of_joining = %s WHERE username = %s"
            mycursor.execute(update_query,(emp_fname_entr.get(),emp_Mname_entr.get(),emp_lname_entr.get(),emp_email_address_entr.get(),emp_contact_no_entr.get(),emp_birth_date_entr.get(),emp_join_date_entr.get(),values[1]))
            resp=messagebox.askyesno("CONFIRMATION","DO YOU WANT TO UPDATE?")
            if resp==1:
                emp_fname_entry.config(text=emp_fname_entr.get())
                emp_Mname_entry.config(text=emp_Mname_entr.get())
                emp_lname_entry.config(text=emp_lname_entr.get())
                emp_email_address_entry.config(text=emp_email_address_entr.get())
                emp_contact_no_entry.config(text=emp_contact_no_entr.get())
                emp_birth_date_entry.config(text=emp_birth_date_entr.get())
                emp_join_date_entry.config(text=emp_join_date_entr.get())
                con.commit()
                messagebox.showinfo("SUCCESS",values[0]+" UPDATED SUCCESSFULLY!")
                cancel_emp_admin()
                reset_user()
                # window.destroy()
            else:
                pass

        emp_submit_button=CTkButton(window,text="SUBMIT",
                                    command=submit_emp_admin,
                                    height=40,
                                    corner_radius=12,
                                    font=("Times New Roman",25,"bold"),
                                    fg_color='#373737',
                                    text_color='#e9e3d5',
                                    hover_color='black')
        emp_submit_button.grid(row=10,column=1)

        # update_query = "UPDATE user SET first_name = %s, last_name = %s, email_address = %s, contact_no = %s, birth_date = %s, date_of_joining = %s WHERE username = %s"
        # mycursor.execute(update_query,(emp_fname_entry.get(),emp_lname_entry.get(),emp_email_address_entry.get(),emp_contact_no_entry.get(),emp_birth_date_entry.get(),emp_join_date_entry.get(),values[1]))
        # con.commit()
        # messagebox.showinfo("SUCCESS","EMPLOYEE DATA UPDATED SUCCESFULLY!")
        # window.destroy()


    emp_update_button=CTkButton(window,text="UPDATE",
                                command=update_emp_admin,
                                height=40,
                                corner_radius=12,
                                font=("Times New Roman",25,"bold"),
                                fg_color='#373737',
                                text_color='#e9e3d5',
                                hover_color='black')
    emp_update_button.grid(row=10,column=1)

    def delete_emp_admin():
        delete_query="DELETE FROM user WHERE username=%s"
        mycursor.execute(delete_query,values[1])
        response=messagebox.askyesno("CONFIRMATION","DO YOU WANT TO DELETE?")
        if response==1:
            con.commit()
            messagebox.showinfo("SUCCESS",values[0]+" DELETED SUCCESSFULLY!")
            window.destroy()
            reset_user()
        else:
            pass
        

    emp_delete_button=CTkButton(window,text="DELETE",
                                command=delete_emp_admin,
                                width=150,
                                height=40,
                                corner_radius=12,
                                font=("Times New Roman",25,"bold"),
                                fg_color='#373737',
                                text_color='#e9e3d5',
                                hover_color='black')
    emp_delete_button.grid(row=10,column=0)

    
    window.mainloop()

employee_view_button=CTkButton(search_button_frame,text="VIEW",command = view_users,width=150,height=40,corner_radius=12,font=("Times New Roman",25,"bold"),fg_color='#373737',text_color='#e9e3d5',hover_color='black')
employee_view_button.grid(row=0,column=2)

admin_page.mainloop()