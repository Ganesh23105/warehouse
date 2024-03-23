# import matplotlib.pyplot as plt
# import numpy as np

# x = np.linspace(-2*np.pi, 2*np.pi, 1000)
# y1 = np.sin(x)
# y2 = np.cos(x)
# y3 = np.tan(x)
# y4 = np.exp(x)
# y5 = np.log(x + np.pi)

# fig = plt.figure()
# ax1 = fig.add_subplot(221)
# ax2 = fig.add_subplot(222)
# ax3 = fig.add_subplot(223)
# ax4 = fig.add_subplot(224)

# ax1.plot(x, y1, color='blue')
# ax2.plot(x, y2, color='red')
# ax3.plot(x, y3, color='green')
# ax4.plot(x, y4, color='purple')

# ax4.plot(x[x > 0], y5[x > 0], color='orange')

# plt.show()




# for 2d representation 

# import matplotlib.pyplot as plt
# import numpy as np

# # Sample warehouse layout (2D grid)
# warehouse_layout = np.zeros((10, 10))  # 10x10 grid, initially empty

# # Sample product locations
# products = [(2, 3), (4, 5), (7, 8)]  # Sample product locations (row, column)

# # Sample product needed
# product_needed = (2, 3)  # For example, product at (2, 3) is needed

# # Update warehouse layout to mark product locations
# for loc in products:
#     warehouse_layout[loc[0], loc[1]] = 1

# # Visualize the warehouse
# plt.imshow(warehouse_layout, cmap='Greens')  # Visualize all products initially as green

# # Mark the needed product as red
# plt.scatter(product_needed[1], product_needed[0], color='red', marker='x')

# plt.title('Virtual Warehouse')
# plt.xlabel('Column')
# plt.ylabel('Row')
# plt.show()

# without rack
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # Sample warehouse layout (3D grid)
# warehouse_layout = np.zeros((10, 10, 10))  # 10x10x10 grid, initially empty

# # Sample product locations
# products = [(2, 3, 4), (4, 5, 6), (7, 8, 9)]  # Sample product locations (x, y, z)

# # Sample product needed
# product_needed = (2, 3, 4)  # For example, product at (2, 3, 4) is needed

# # Update warehouse layout to mark product locations
# for loc in products:
#     warehouse_layout[loc[0], loc[1], loc[2]] = 1

# # Create 3D figure
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# # Plot products
# x, y, z = np.nonzero(warehouse_layout)
# ax.scatter(x, y, z, color='g', marker='o', label='Products')

# # Mark the needed product as red
# ax.scatter(*product_needed, color='r', marker='x', s=100, label='Needed Product')

# # Set labels and title
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('Virtual Warehouse')

# # Add legend
# ax.legend()

# # Show plot
# plt.show()

# with rack

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def plot_warehouse(warehouse_layout, products, product_needed):
#     fig = plt.figure(figsize=(10, 8))
#     ax = fig.add_subplot(111, projection='3d')

#     # Plot products
#     x, y, z = np.nonzero(warehouse_layout)
#     ax.scatter(x, y, z, color='g', marker='o', label='Products')

#     # Plot shelves (for demonstration purposes, you may need to adjust this based on your layout)
#     for i in range(warehouse_layout.shape[0]):
#         for j in range(warehouse_layout.shape[1]):
#             for k in range(warehouse_layout.shape[2]):
#                 if warehouse_layout[i, j, k] == 0:
#                     ax.scatter(i, j, k, color='k', marker='_')

#     # Mark the needed product as red
#     ax.scatter(*product_needed, color='r', marker='x', s=100, label='Needed Product')

#     # Set labels and title
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')
#     ax.set_title('Virtual Warehouse')

#     # Add legend
#     ax.legend()

#     plt.show()

# # Sample warehouse layout (3D grid)
# warehouse_layout = np.zeros((10, 10, 10))  # 10x10x10 grid, initially empty

# # Sample product locations
# products = [(2, 3, 4), (4, 5, 6), (7, 8, 9)]  # Sample product locations (x, y, z)

# # Sample product needed
# product_needed = (2, 3, 4)  # For example, product at (2, 3, 4) is needed

# # Update warehouse layout to mark product locations
# for loc in products:
#     warehouse_layout[loc[0], loc[1], loc[2]] = 1

# plot_warehouse(warehouse_layout, products, product_needed)


from vpython import box, color, vector, rate

# Function to create a rack
def create_rack(pos):
    rack = box(pos=pos, size=vector(1, 2, 1), color=color.red)  # Adjust size of rack to make it more visible
    for i in range(1, 10, 2):  # Adding shelves to the rack
        shelf = box(pos=pos + vector(0, i * 0.1, 0), size=vector(1, 0.1, 1), color=color.gray(0.8))
    return rack

# Create walls of the room with white color
left_wall = box(pos=vector(-5, 0, 0), size=vector(0.1, 10, 10), color=color.white)
right_wall = box(pos=vector(5, 0, 0), size=vector(0.1, 10, 10), color=color.white)
back_wall = box(pos=vector(0, 0, -5), size=vector(10, 10, 0.1), color=color.white)
front_wall = box(pos=vector(0, 0, 5), size=vector(10, 10, 0.1), color=color.white)
ceiling = box(pos=vector(0, 5, 0), size=vector(10, 0.1, 10), color=color.white)
floor = box(pos=vector(0, -5, 0), size=vector(10, 0.1, 10), color=color.white)

# Add racks to the room
rack1 = create_rack(vector(-3, 1, -3))  # Adjust y-coordinate to position rack properly
rack2 = create_rack(vector(3, 1, -3))   # Adjust y-coordinate to position rack properly
rack3 = create_rack(vector(-3, 1, 3))   # Adjust y-coordinate to position rack properly
rack4 = create_rack(vector(3, 1, 3))    # Adjust y-coordinate to position rack properly

# Run the VPython event loop
while True:
    rate(30)  # Limit to 30 frames per second
