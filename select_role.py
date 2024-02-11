from tkinter import *
from PIL import Image, ImageTk

def employee_page():
    select_role.destroy()
    import employee_login_registration

def admin_page():
     select_role.destroy()
     import admin_login_registration

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

select_role = Tk()
select_role.geometry('1200x650')
select_role.title('Images')
select_role.minsize(1200,650)

# grid layout
select_role.columnconfigure(0, weight = 1, uniform = 'a')
select_role.rowconfigure(0, weight = 1)

# import an image 
image_original = Image.open('image\\select_role.jpg')
image_ratio = image_original.size[0] / image_original.size[1]
image_tk = ImageTk.PhotoImage(image_original)

canvas = Canvas(select_role, background = 'black', bd = 0, highlightthickness = 0, relief = 'ridge')
canvas.grid(column = 0, row = 0, sticky = 'nsew')

canvas.bind('<Configure>', fill_image)

sample_label=Label(select_role,background="white")
sample_label.place(relx=0.75,rely=0.5,anchor='center')

select_role_name_label=Label(sample_label,text="SELECT A ROLE",bg="white",font=("Times New Roman",40,"bold"),fg="#373737")
select_role_name_label.grid(row=0,column=0,padx=5)

role_admin_button=Button(sample_label,text="EMPLOYEE",command=employee_page, bd=0,font=("Times New Roman",25,"bold"),bg="#373737",cursor="hand2",fg="white",activeforeground='#373737')
role_admin_button.grid(row=1,column=0,padx=50,pady=20)

role_staff_button=Button(sample_label,text="ADMIN",command=admin_page, bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
role_staff_button.grid(row=3,column=0,padx=50,pady=20)

# run
select_role.mainloop()
