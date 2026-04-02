import mysql.connector
from tkinter import *

# ---------------- DATABASE CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="prathamesh",
    password="1234",
    database="food_db"
)

cursor = conn.cursor()

print("Connected to MySQL ✅")

# ---------------- FUNCTIONS ----------------
def get_menu():
    cursor.execute("SELECT * FROM menu")
    return cursor.fetchall()

def place_order(name, qty, price):
    total = qty * price
    cursor.execute(
        "INSERT INTO orders (item_name, quantity, total_price) VALUES (%s, %s, %s)",
        (name, qty, total)
    )
    conn.commit()

def get_orders():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()

# ---------------- GUI ----------------
root = Tk()
root.title("Food Order System")
root.geometry("400x400")

# Menu List
menu_list = Listbox(root)

for item in get_menu():
    menu_list.insert(END, f"{item[1]} - ₹{item[2]}")

menu_list.pack()

# Quantity Input
Label(root, text="Enter Quantity").pack()
qty_entry = Entry(root)
qty_entry.pack()

# Order Function
def order_now():
    if not menu_list.curselection():
        print("Select item first")
        return

    if not qty_entry.get():
        print("Enter quantity")
        return

    selected = menu_list.get(menu_list.curselection())
    qty = int(qty_entry.get())

    name, price = selected.split(" - ₹")
    place_order(name, qty, int(price))

    print("Order placed ✅")

# Buttons
Button(root, text="Order Now", command=order_now).pack()

def show_bill():
    print("\n--- BILL ---")
    for order in get_orders():
        print(order)

Button(root, text="Show Bill", command=show_bill).pack()

# Run App
root.mainloop()