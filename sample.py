from tkinter import *
from tkinter.ttk import Combobox, Treeview

search_frame=Tk()

attributes_frame = Frame(search_frame)
attributes_frame.place(relx=0,rely=0,relwidth=1,relheight=0.25)

employee_role_label=Label(attributes_frame,text="ROLE")
employee_role_label.grid(row=0,column=0)
search_role_combo_var=StringVar()
search_role_combo_box = Combobox(attributes_frame,textvariable=search_role_combo_var,state="readonly")
search_role_combo_box['values'] = ('Admin', 'Employee')
search_role_combo_box.grid(row=0,column=1)
search_role_combo_box.set("Select")

employee_username_label=Label(attributes_frame,text="USERNAME")
employee_username_label.grid(row=1,column=0)
employee_username_entry=Entry(attributes_frame)
employee_username_entry.grid(row=1,column=1)

employee_year_label=Label(attributes_frame,text="YEAR")
employee_year_label.grid(row=2,column=0)
employee_year_entry=Entry(attributes_frame)
employee_year_entry.grid(row=2,column=1)   

employee_month_label=Label(attributes_frame,text="MONTH")
employee_month_label.grid(row=2,column=4)
employee_month_entry=Entry(attributes_frame)
employee_month_entry.grid(row=2,column=6) 

employee_reset_button=Button(attributes_frame,text="RESET")
employee_reset_button.grid(row=3,column=1)

employee_select_button=Button(attributes_frame,text="SEARCH")
employee_select_button.grid(row=3,column=2)

tree_scroll_frame = Frame(search_frame)
tree_scroll_frame.place(relx=0,rely=0.25,relwidth=1,relheight=0.75)

tree = Treeview(tree_scroll_frame, columns=(1,2,3,4,5,6,7,8), show="headings")
tree.heading(1, text="ROLE")
tree.heading(2, text="USERNAME")
tree.heading(3, text="FIRST_NAME")
tree.heading(4, text="LAST_NAME")
tree.heading(5, text="EMAIL_ADDRESS")
tree.heading(6, text="CONTACT_NO")
tree.heading(7, text="BIRTH_DATE")
tree.heading(8, text="JOINING_DATE")

# tree_y_scroll = Scrollbar(search_frame, orient="vertical", command=tree.yview)
# tree.configure(yscrollcommand=tree_y_scroll.set)
# tree_y_scroll.grid(row=4, column=5,sticky="ns")

tree_x_scroll = Scrollbar(tree_scroll_frame, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=tree_x_scroll.set)
tree_x_scroll.pack(side='bottom',fill=X)

tree.pack()

search_frame.mainloop()