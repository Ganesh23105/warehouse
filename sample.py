import tkinter as tk

# Define colors
WHITE = "#FFFFFF"
GRAY = "#C0C0C0"
BLACK = "#000000"

# Define cube dimensions
CUBE_SIZE = 50

# Define initial warehouse dimensions
INITIAL_NUM_RACKS = 1
NUM_SHELVES = 5

class Product:
    def _init_(self, name, quantity):
        self.name = name
        self.quantity = quantity

def draw_cube(canvas, x, y, z, color=GRAY):
    # Draw top face
    canvas.create_polygon(x, y, x + CUBE_SIZE, y, x + CUBE_SIZE, y + CUBE_SIZE, x, y + CUBE_SIZE, fill=color)

    # Draw left face
    canvas.create_polygon(x, y, x, y + CUBE_SIZE, x, y + CUBE_SIZE + z, x, y + z, fill=color, outline=BLACK)

    # Draw right face
    canvas.create_polygon(x + CUBE_SIZE, y, x + CUBE_SIZE, y + CUBE_SIZE, x + CUBE_SIZE, y + CUBE_SIZE + z, x + CUBE_SIZE, y + z, fill=color, outline=BLACK)

    # Draw front face
    canvas.create_polygon(x, y + CUBE_SIZE, x + CUBE_SIZE, y + CUBE_SIZE, x + CUBE_SIZE, y + CUBE_SIZE + z, x, y + CUBE_SIZE + z, fill=color, outline=BLACK)

def draw_warehouse(canvas, num_racks):
    canvas.delete("all")
    canvas_width = (CUBE_SIZE + 10) * num_racks
    canvas_height = (CUBE_SIZE + 10) * NUM_SHELVES * 2  # Double canvas height for upper and lower part
    for i in range(num_racks):
        for j in range(NUM_SHELVES):
            draw_cube(canvas, i * (CUBE_SIZE + 10), j * (CUBE_SIZE + 10), 50)
    canvas.config(width=canvas_width, height=canvas_height)

def add_rack(canvas):
    global INITIAL_NUM_RACKS
    INITIAL_NUM_RACKS += 1
    draw_warehouse(canvas, INITIAL_NUM_RACKS)

def change_row(canvas):
    global NUM_SHELVES
    NUM_SHELVES += 1
    canvas_height = (CUBE_SIZE + 10) * NUM_SHELVES * 2  # Double canvas height for upper and lower part
    canvas.config(height=canvas_height)

def main():
    root = tk.Tk()
    root.title("3D Warehouse Visualization")

    canvas = tk.Canvas(root, bg=WHITE)
    canvas.pack(expand=True, fill="both")

    draw_warehouse(canvas, INITIAL_NUM_RACKS)

    add_rack_button = tk.Button(root, text="Add", command=lambda: add_rack(canvas))
    add_rack_button.pack()

    change_row_button = tk.Button(root, text="Change Row", command=lambda: change_row(canvas))
    change_row_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()