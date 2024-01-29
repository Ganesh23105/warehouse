from tkinter import *
from customtkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk

def place_frame(event):
    width = event.width
    height = event.height

    x = 900/450 * width
    y = 650/200 * height
    # return (x,y)
    print(width,' ',height)

def stretch_image(event):

    global resized_tk
    #size
    width = event.width
    height = event.height

    #create image
    resized_image = bgOriginal.resize((width,height))
    resized_tk = ImageTk.PhotoImage(resized_image)

    #place on the canvas
    canvas.create_image(0,0, image=resized_tk, anchor='nw')


def fill_image(event):
    global resized_tk

    #current ratio
    canvas_ratio = event.width / event.height

    if canvas_ratio > bgRatio :
        width = int(event.width)
        height = int(width / bgRatio)

    else:
        height = int(event.height)
        width = int(height * bgRatio)

    resized_image = bgOriginal.resize((width,height))
    resized_tk = ImageTk.PhotoImage(resized_image)
    canvas.create_image(
        int(event.width /2), 
        int(event.height)/2, 
        anchor = 'center', 
        image = resized_tk)

def admin_page():
    select_role.destroy()
    import employee_login_registration

# def staff_page():
#      select_role.destroy()
#      import staff_login_registration

# def registration_page():
#     select_role.destroy()
#     import manager_login_registration

select_role=Tk()
select_role.title("WAREHOUSE")
select_role.geometry("900x650")

select_role.columnconfigure(0,weight=1)
select_role.rowconfigure(0,weight=1)

bgOriginal = Image.open('image\\first.jpg')
bgRatio = bgOriginal.size[0] / bgOriginal.size[1]
# print(bgRatio)
bgImage = ImageTk.PhotoImage(bgOriginal)

canvas = Canvas(select_role,bd=0,highlightthickness=0, relief='ridge')
canvas.grid(column=0, row=0, sticky='nsew')
# canvas.create_image(0,0, image=bgImage, anchor='nw')
canvas.bind('<Configure>',fill_image)

sample_frame=Frame(canvas)
# sample_frame.configure(background='systemTransparent')
obj = sample_frame.bind('<Configure>', place_frame)
sample_frame.place(x=obj[0],y=obj[1])


sample_label2=Label(sample_frame,text="Select a role")
sample_label2.grid(row=0,column=0,padx=5)

role_admin_button=CTkButton(sample_frame,text="Employee",command=admin_page)
role_admin_button.grid(row=1,column=0,padx=50,pady=20)

# role_staff_button=Button(sample_label,text="Admin",command=staff_page, bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
# role_staff_button.grid(row=3,column=0,padx=50,pady=20)

# role_manager_button=Button(sample_label,text="MANAGER",command=registration_page, bd=0,font=("Times New Roman",25,"bold"),width=10,bg="#373737",fg="white",activeforeground='#373737')
# role_manager_button.grid(row=5,column=0,padx=50,pady=20)

select_role.mainloop()