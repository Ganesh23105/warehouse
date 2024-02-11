import pymysql

# Connect to the MySQL database
connection = pymysql.connect(
    host='your_host',
    user='your_username',
    password='your_password',
    database='your_database'
)

# Create a cursor object
cursor = connection.cursor()

# Read the image file as binary data
with open('image.jpg', 'rb') as file:
    image_data = file.read()

# Define the SQL query to create a new table with a BLOB column
create_table_query = """
CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_data BLOB
)
"""

# Execute the create table query
cursor.execute(create_table_query)

# Define the SQL query to insert data into the table
insert_query = """
INSERT INTO images (image_data)
VALUES (%s)
"""

# Execute the insert query with the image data
cursor.execute(insert_query, (image_data,))

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
