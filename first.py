from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *
from tkinter import messagebox
import pymysql
import cv2
from pyzbar.pyzbar import decode
import warnings

def employee_page():
    select_role.destroy()
    import employee_page

def admin_page():
    select_role.destroy()
    import admin_page

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

def hide():
    global eye_img, eye_img_og
    eye_img_og = Image.open('image\\close_eye.png').resize((55,55))
    eye_img = ImageTk.PhotoImage(eye_img_og)
    password_entry.configure(show='*')
    eye_btn.configure(image=eye_img)
    eye_btn.config(command=show)
    
def show():
    global eye_img_og, eye_img
    eye_img_og = Image.open('image\\open_eye.png').resize((55,55))
    eye_img = ImageTk.PhotoImage(eye_img_og)
    password_entry.configure(show='')
    eye_btn.config(image=eye_img)
    eye_btn.config(command=hide)

def login():
    select_role_combobox.configure(state='normal')
    if username_entry.get() == "" or password_entry.get() == "":
        messagebox.showerror("ERROR", "All fields should be filled.")
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='root')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection is not established try again.')
            return
		
        query = 'use warehouse'
        mycursor.execute(query)
        query = 'select * from user where username=%s'
        mycursor.execute(query, (username_entry.get()))
        row = mycursor.fetchone()

        if row == None:
            messagebox.showerror('Error', 'INVALID USERNAME')
            select_role_combobox.configure(state='readonly')
        elif str(select_role_combobox.get())[0] != row[2][0]:
            messagebox.showerror('Error', 'INVALID ROLE')
            select_role_combobox.configure(state='readonly')
        elif password_entry.get() != row[1]:
            messagebox.showerror('ERROR', 'INVALID PASSWORD')
            select_role_combobox.configure(state='readonly')
        else:
            messagebox.showinfo('Success', 'LOGIN SUCCESSFUL')
            select_role_combobox.configure(state='readonly')
            # select_role.destroy()
            if row[2] == 'Admin':
                admin_page()
            else: 
            	employee_page()

def scan_qr():

    # Suppress ZBar PDF417 warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="pyzbar.pyzbar")

    try:
        # Connect to the database
        con = pymysql.connect(host='localhost', user='root', password='root')
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error', 'Connection is not established. Please try again.')
        return    

    query = 'use warehouse'
    mycursor.execute(query) 

    # Create a VideoCapture object (0 for default camera)
    cap = cv2.VideoCapture(0) 

    # Set window flags to disable close, minimize, maximize buttons
    cv2.namedWindow("QR Code Scanner", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)

    # Initialize flag variable outside the loop
    flag = None  

    while flag is None:  # Continue looping until the flag is set

        # Capture frames from the camera
        ret, frame = cap.read()

        # Decode QR code
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            data = obj.data.decode('utf-8')

            # create a list
            list_data = list(data.split('\n'))

            # Verify against the database
            query = 'select * from user where role = %s AND first_name = %s AND middle_name = %s AND last_name = %s AND birth_date = %s AND date_of_joining = %s'
            mycursor.execute(query, (list_data[0], list_data[1], list_data[2], list_data[3], list_data[4], list_data[5]))
            result = mycursor.fetchone()

            if result:              
                if list_data[0] == 'Admin':
                    flag = 'a'
                else:
                    flag = 'e'
                break
            else:
                print("QR Code not found in the database.")

        # Display the frame
        cv2.imshow("QR Code Scanner", frame)

        # Break the loop if the escape key (27) is pressed
        if cv2.waitKey(1) == 27:
            break

    # Release the VideoCapture and close the connection
    cap.release()
    mycursor.close()
    con.close()

    # Destroy the OpenCV window
    cv2.destroyWindow("QR Code Scanner")

    if flag == 'a':
        select_role.destroy()
        import admin_page
    elif flag == 'e':
        select_role.destroy()
        import employee_page
  
select_role = Tk()
select_role.geometry('1200x650')
select_role.title('Images')
select_role.minsize(1200,650)
select_role.configure(bg='#e9e3d5')

# grid layout
select_role.columnconfigure(0, weight = 1, uniform = 'a')
select_role.rowconfigure(0, weight = 1)

# import an image 
image_original = Image.open('image\\select_role.png')
image_ratio = image_original.size[0] / image_original.size[1]
image_tk = ImageTk.PhotoImage(image_original)

canvas = Canvas(select_role, 
                background = 'black', 
                bd = 0, 
                highlightthickness = 0, 
                relief = 'ridge')
canvas.grid(column = 0, row = 0, sticky = 'nsew')

canvas.bind('<Configure>', fill_image)

qr_label = CTkLabel(select_role,
                  text='',
                  fg_color='#373737',
                  corner_radius=30)
qr_label.place(relx=0.85,rely=0.1,anchor='w',relwidth=0.1,relheight=0.15)
qr_img = Image.open('image\\qr_img.png').resize((80,80))
cam_img = ImageTk.PhotoImage(qr_img)
cam_btn = Button(select_role,
                 width=75,
                 height=75,
                 image=cam_img,
                 bd=0,
                 command=scan_qr)
cam_btn.place(relx=0.9,rely=0.1,anchor='center')

main_frame = CTkFrame(select_role,
                    fg_color="#e9e3d5")
main_frame.place(relx=0.54,rely=0.25,relwidth=0.45,relheight=0.5)

# main_frame.rowconfigure((0,1,2,3), weight = 1, uniform = 'a')
# main_frame.columnconfigure((0,1),weight=1,uniform='a')

select_role_name_label = CTkLabel(main_frame,
                                text="SELECT A ROLE                                   ",
                                fg_color="white",
                                font=("Times New Roman",28,"bold"),
                                text_color="#373737",
                                corner_radius=25)
select_role_name_label.place(relx=0.05,rely=0.1,anchor='w',relwidth=0.95,relheight=0.20)

combobox_var = StringVar(value="SELECT")
select_role_combobox = CTkComboBox(main_frame, 
								   values=["ADMIN", "EMPLOYEE"],
								   width=250,height=50,
								   corner_radius=15,
								   fg_color='#e9e3d5',text_color='#373737',
								   border_color='#373737',
								   button_color='#373737',
								   font=("Times New Roman",20,"bold"),
								   button_hover_color='#e9e3d5',
								   dropdown_fg_color='white',
								   dropdown_hover_color='#e9e3d5',
								   dropdown_font=("Times New Roman",15,"bold"),
								   dropdown_text_color='#373737',
								   justify='center',
								   variable=combobox_var,
								   state='readonly',
								   border_width=3				   
								   )
select_role_combobox.place(relx=0.75,rely=0.1,anchor='center')

username_label = CTkLabel(main_frame,
                          text="USERNAME                                ",
                          fg_color="white",
                          font=("Times New Roman",25,"bold"),
                          text_color="#373737",
                          corner_radius=25)
username_label.place(rely=0.45,relx=0.09,anchor='w',relwidth=0.8,relheight=0.15)
username_entry = CTkEntry(main_frame,
                          width=185,
                          height=35,
                          corner_radius=10.5,
                          border_color='#373737',
                          fg_color='#e9e3d5',
                          text_color='#373737',
                          font=("Times New Roman",14,"bold"))
username_entry.place(relx=0.69,rely=0.45,anchor='center')

password_label = CTkLabel(main_frame,
                          text="PASSWORD                                ",
                          fg_color="white",
                          font=("Times New Roman",25,"bold"),
                          text_color="#373737",
                          corner_radius=25)
password_label.place(rely=0.625,relx=0.09,anchor='w',relwidth=0.8,relheight=0.15)
password_entry = CTkEntry(main_frame,
                          width=185,
                          height=35,
                          corner_radius=10.5,
                          border_color='#373737',
                          show='*',
                          fg_color='#e9e3d5',
                          text_color='#373737',
                          font=("Times New Roman",14,"bold"))
password_entry.place(relx=0.69,rely=0.625,anchor='center')

login_btn = CTkButton(main_frame,
                      text='LOGIN',
                      command=login ,
                      width=150,
                      height=40,
                      corner_radius=12,
                      font=("Times New Roman",25,"bold"),
                      fg_color='#373737',
                      text_color='#e9e3d5',
                      hover_color='white')
login_btn.place(relx=0.5,rely=0.85,anchor='center')

# openeye = PhotoImage(file='openeye.png')
eye_img_og = Image.open('image\\close_eye.png').resize((55,55))
eye_img = ImageTk.PhotoImage(eye_img_og)
eye_btn = Button(main_frame,
                 image=eye_img,
                 bd=0,
                 cursor='hand2',
                 bg='#e9e3d5',
                 activebackground='#e9e3d5',
                 command = show)
eye_btn.place(rely=0.625,relx=0.9,anchor='w',relwidth=0.1,relheight=0.16)

# run
select_role.mainloop()
