import tkinter as tk
from tkinter import ttk

class ScrollableCombobox:
    def __init__(self, master, values, dropdown_height=10):
        self.master = master
        self.values = values
        self.dropdown_height = dropdown_height

        self.combobox_frame = ttk.Frame(master)
        self.combobox_frame.pack(fill='x')

        self.combobox = ttk.Combobox(self.combobox_frame)
        self.combobox.pack(side='left', fill='x', expand=True)
        self.combobox.bind('<Button-1>', self.show_dropdown)

        self.dropdown = None
        self.create_dropdown()

    def create_dropdown(self):
        self.dropdown = tk.Listbox(self.combobox_frame, height=self.dropdown_height)
        self.dropdown_scrollbar = tk.Scrollbar(self.combobox_frame, orient='vertical', command=self.dropdown.yview)
        self.dropdown.config(yscrollcommand=self.dropdown_scrollbar.set)

        for value in self.values:
            self.dropdown.insert('end', value)

        self.dropdown.bind('<Double-Button-1>', self.select_item)

    def show_dropdown(self, event=None):
        self.dropdown.place(in_=self.combobox, relx=0, rely=1, relwidth=1)
        self.dropdown_scrollbar.pack(side='right', fill='y')

    def hide_dropdown(self):
        self.dropdown.place_forget()
        self.dropdown_scrollbar.pack_forget()

    def select_item(self, event=None):
        selected_index = self.dropdown.curselection()
        if selected_index:
            selected_index = int(selected_index[0])  # Convert to integer
            selected_value = self.values[selected_index]
            self.combobox.set(selected_value)
        self.hide_dropdown()

root = tk.Tk()
root.geometry("300x200")

values = [str(i) for i in range(1000)]  # Example: 1000 values

scrollable_combobox = ScrollableCombobox(root, values, dropdown_height=5)  # Set dropdown height to 5

root.mainloop()
