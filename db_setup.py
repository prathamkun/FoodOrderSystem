import mysql.connector
from mysql.connector import Error

def create_database_and_tables():
    print("Connecting to MySQL server...")
    try:
        # First connect without database to create it if it doesn't exist
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password=''  # Default MAMP/XAMPP or local install without password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            print("Connected to MySQL Server.")
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS mini_zomato_db;")
            print("Database mini_zomato_db created or already exists.")
            
            # Switch to the database
            cursor.execute("USE mini_zomato_db;")
            
            # Create menu table
            create_menu_table = """
            CREATE TABLE IF NOT EXISTS menu (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(50) NOT NULL,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            );
            """
            cursor.execute(create_menu_table)
            print("Table 'menu' ready.")

            # Create orders table
            create_orders_table = """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_orders_table)
            print("Table 'orders' ready.")

            # Create order_items table
            create_order_items_table = """
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                item_id INT NOT NULL,
                quantity INT NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (item_id) REFERENCES menu(item_id)
            );
            """
            cursor.execute(create_order_items_table)
            print("Table 'order_items' ready.")

            # Check if menu has data, otherwise insert default items
            cursor.execute("SELECT COUNT(*) FROM menu;")
            count = cursor.fetchone()[0]
            if count == 0:
                print("Populating menu with initial items...")
                initial_items = [
                    ('Pizza', 'Margherita Pizza', 250.00),
                    ('Pizza', 'Pepperoni Pizza', 350.00),
                    ('Burger', 'Veggie Burger', 150.00),
                    ('Burger', 'Chicken Burger', 200.00),
                    ('Pasta', 'White Sauce Pasta', 220.00),
                    ('Pasta', 'Red Sauce Pasta', 210.00),
                    ('Beverages', 'Coke', 60.00),
                    ('Beverages', 'Cold Coffee', 120.00),
                    ('Dessert', 'Chocolate Brownie', 150.00),
                    ('Dessert', 'Ice Cream', 80.00)
                ]
                insert_query = "INSERT INTO menu (category, name, price) VALUES (%s, %s, %s)"
                cursor.executemany(insert_query, initial_items)
                connection.commit()
                print(f"Inserted {cursor.rowcount} items into menu.")
            else:
                print("Menu table already has valid items.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    create_database_and_tables()
