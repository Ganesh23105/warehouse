import pymysql
import random
import string

# Function to generate random product IDs
def generate_product_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Function to generate random product names for electronic appliances
def generate_product_name():
    products = ['Refrigerator', 'Television', 'Air Conditioner', 'Washing Machine', 'Microwave Oven']
    return random.choice(products)

# Function to generate random brands for electronic appliances
def generate_brand():
    brands = ['LG', 'Samsung', 'Whirlpool', 'Sony', 'Voltas']
    return random.choice(brands)

# Function to generate random categories for electronic appliances
def generate_category():
    categories = ['Refrigerators', 'Televisions', 'Air Conditioners', 'Washing Machines', 'Microwave Ovens']
    return random.choice(categories)

# Function to generate random locations
def generate_location():
    locations = ['Warehouse 1', 'Warehouse 2', 'Warehouse 3', 'Warehouse 4', 'Warehouse 5']
    return random.choice(locations)

# Function to generate random quantities
def generate_quantity():
    return str(random.randint(1, 100))

# Connect to MySQL database
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       database='warehouse',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

try:
    with conn.cursor() as cursor:
        # Delete existing data from the table
        cursor.execute("DELETE FROM products")

        # Generate and insert new random data for electronic appliances
        for _ in range(10000):  # Adjust the number as needed
            product_id = generate_product_id()
            product_name = generate_product_name()
            brand = generate_brand()
            category = generate_category()
            location = generate_location()
            quantity = generate_quantity()

            cursor.execute("INSERT INTO products VALUES (%s, %s, %s, %s, %s, %s)",
                           (product_id, product_name, brand, category, location, quantity))
    
    # Commit changes
    conn.commit()
    print("Data inserted successfully.")
finally:
    # Close connection
    conn.close()
