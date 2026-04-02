import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------- DATABASE ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="prathamesh",
    password="1234",
    database="food_db"
)

cursor = conn.cursor()

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
root.geometry("600x600")
root.configure(bg="#ff7f50")

# Title
Label(root, text="🍔 Food Order System", font=("Arial", 20, "bold"),
      bg="#ff7f50", fg="white").pack(pady=10)

# ---------------- IMAGES ----------------
frame = Frame(root, bg="#ff7f50")
frame.pack()

def load_img(name):
    img = Image.open(name)
    img = img.resize((80, 80))
    return ImageTk.PhotoImage(img)

burger_img = load_img("burger.png")
pizza_img = load_img("pizza.png")
pasta_img = load_img("pasta.png")
sandwich_img = load_img("sandwich.png")

Label(frame, image=burger_img, bg="#ff7f50").grid(row=0, column=0, padx=10)
Label(frame, image=pizza_img, bg="#ff7f50").grid(row=0, column=1, padx=10)
Label(frame, image=pasta_img, bg="#ff7f50").grid(row=0, column=2, padx=10)
Label(frame, image=sandwich_img, bg="#ff7f50").grid(row=0, column=3, padx=10)

# ---------------- MENU LIST ----------------
menu_list = Listbox(root, font=("Arial", 12), width=30, height=6)

for item in get_menu():
    menu_list.insert(END, f"{item[1]} - ₹{item[2]}")

menu_list.pack(pady=10)

# ---------------- QUANTITY ----------------
Label(root, text="Enter Quantity", bg="#ff7f50", fg="white").pack()
qty_entry = Entry(root, font=("Arial", 12))
qty_entry.pack(pady=5)

# ---------------- ORDER FUNCTION ----------------
def order_now():
    if not menu_list.curselection():
        messagebox.showerror("Error", "Select item first")
        return

    if not qty_entry.get():
        messagebox.showerror("Error", "Enter quantity")
        return

    selected = menu_list.get(menu_list.curselection())
    qty = int(qty_entry.get())

    name, price = selected.split(" - ₹")
    place_order(name, qty, int(price))

    messagebox.showinfo("Success", f"{name} ordered successfully!")

# ---------------- BILL FUNCTION ----------------
def show_bill():
    orders = get_orders()

    if not orders:
        messagebox.showinfo("Bill", "No orders yet")
        return

    bill_text = ""
    total = 0

    for order in orders:
        bill_text += f"{order[1]} x{order[2]} = ₹{order[3]}\n"
        total += order[3]

    bill_text += f"\nTotal = ₹{total}"

    messagebox.showinfo("Your Bill", bill_text)

# ---------------- BUTTONS ----------------
Button(root, text="Order Now", bg="white", fg="orange",
       font=("Arial", 12), command=order_now).pack(pady=10)

Button(root, text="Show Bill", bg="white", fg="orange",
       font=("Arial", 12), command=show_bill).pack()

# ---------------- RUN ----------------
root.mainloop()