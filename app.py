import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import os
try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Error", "Pillow is not installed. Please run pip install Pillow")

class MiniZomatoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Zomato - Food Order System")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f4f4")
        
        self.cart_items = {} # {item_id: {'name': name, 'price': price, 'quantity': qty, 'subtotal': sub}}
        self.photo_cache = {}
        
        self.create_db_connection()
        self.create_gui()
        self.load_menu()
        
    def get_image_for_category(self, category):
        # Expected categories: Pizza, Burger, Pasta. Fallback to default
        path = f"assets/{category}.png"
        if not os.path.exists(path):
            return None
        
        if category not in self.photo_cache:
            try:
                img = Image.open(path)
                img = img.resize((250, 250), Image.Resampling.LANCZOS)
                self.photo_cache[category] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Failed to load image {path}: {e}")
                return None
            
        return self.photo_cache[category]

    def create_db_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='mini_zomato_db'
            )
        except Error as e:
            messagebox.showerror("Database Error", f"Cannot connect to Database: {e}")
            self.root.destroy()

    def create_gui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#cb202d", pady=10) # Zomato Red
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="Mini Zomato", font=("Helvetica", 24, "bold"), fg="white", bg="#cb202d")
        header_label.pack()

        # Main Layout: 3 Columns
        main_frame = tk.Frame(self.root, bg="#f4f4f4", pady=10, padx=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ################ COL 1: Menu ################
        left_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        menu_label = tk.Label(left_frame, text="Menu Directory", font=("Helvetica", 16, "bold"), bg="white")
        menu_label.pack(pady=(0, 10))

        # Menu Treeview
        columns = ("id", "category", "name", "price")
        self.menu_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        self.menu_tree.heading("id", text="ID")
        self.menu_tree.heading("category", text="Category")
        self.menu_tree.heading("name", text="Item Name")
        self.menu_tree.heading("price", text="Price")
        
        self.menu_tree.column("id", width=30)
        self.menu_tree.column("category", width=80)
        self.menu_tree.column("name", width=160)
        self.menu_tree.column("price", width=70)
        
        self.menu_tree.pack(fill=tk.BOTH, expand=True)
        self.menu_tree.bind("<<TreeviewSelect>>", self.on_menu_select)

        # Actions under Menu
        action_frame = tk.Frame(left_frame, bg="white", pady=10)
        action_frame.pack(fill=tk.X)

        tk.Label(action_frame, text="Qty:", bg="white", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.qty_var = tk.IntVar(value=1)
        qty_spin = ttk.Spinbox(action_frame, from_=1, to=20, textvariable=self.qty_var, width=3)
        qty_spin.pack(side=tk.LEFT, padx=(5, 10))
        
        add_btn = tk.Button(action_frame, text="Add to Cart", command=self.add_to_cart, bg="#4CAF50", fg="black", font=("Helvetica", 11, "bold"))
        add_btn.pack(side=tk.LEFT)
        
        manage_menu_btn = tk.Button(action_frame, text="+ Add Product", command=self.open_add_product_window, fg="blue", bg="white", relief=tk.FLAT, font=("Helvetica", 10, "underline"))
        manage_menu_btn.pack(side=tk.RIGHT)

        ################ COL 2: Image Preview ################
        mid_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10, relief=tk.RAISED, borderwidth=1, width=280)
        mid_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 5))
        mid_frame.pack_propagate(False) # Prevent shrinking automatically
        
        preview_title = tk.Label(mid_frame, text="Item Preview", font=("Helvetica", 16, "bold"), bg="white")
        preview_title.pack(pady=(0, 10))
        
        self.img_label = tk.Label(mid_frame, bg="white", text="Select an item...", font=("Helvetica", 10, "italic"))
        self.img_label.pack(expand=True)
        
        self.desc_label = tk.Label(mid_frame, text="", font=("Helvetica", 14, "bold"), bg="white", wraplength=250)
        self.desc_label.pack(pady=10)


        ################ COL 3: Cart & Checkout ################
        right_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        cart_label = tk.Label(right_frame, text="Your Cart", font=("Helvetica", 16, "bold"), bg="white")
        cart_label.pack(pady=(0, 10))

        # Cart Treeview
        cart_columns = ("id", "name", "qty", "subtotal")
        self.cart_tree = ttk.Treeview(right_frame, columns=cart_columns, show="headings", height=10)
        self.cart_tree.heading("id", text="ID")
        self.cart_tree.heading("name", text="Item Name")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("subtotal", text="Subtotal")

        self.cart_tree.column("id", width=30)
        self.cart_tree.column("name", width=180)
        self.cart_tree.column("qty", width=50)
        self.cart_tree.column("subtotal", width=80)

        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        remove_btn = tk.Button(right_frame, text="Remove Selected", command=self.remove_from_cart, fg="black")
        remove_btn.pack(pady=5, anchor=tk.E)

        # Total and Checkout
        checkout_frame = tk.Frame(right_frame, bg="white", pady=10)
        checkout_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.total_lbl = tk.Label(checkout_frame, text="Total: ₹0.00", font=("Helvetica", 14, "bold"), bg="white", fg="green")
        self.total_lbl.pack(anchor=tk.E, pady=(0, 10))

        payment_frame = tk.Frame(checkout_frame, bg="white")
        payment_frame.pack(fill=tk.X)

        tk.Label(payment_frame, text="Customer Name:", bg="white", font=("Helvetica", 10)).pack(side=tk.LEFT)
        self.customer_name_var = tk.StringVar()
        tk.Entry(payment_frame, textvariable=self.customer_name_var, width=15).pack(side=tk.LEFT, padx=5)

        place_order_btn = tk.Button(payment_frame, text="Place Order", command=self.place_order, bg="#cb202d", fg="black", font=("Helvetica", 12, "bold"))
        place_order_btn.pack(side=tk.RIGHT)

    def load_menu(self):
        # Clear existing
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM menu")
            rows = cursor.fetchall()
            for row in rows:
                self.menu_tree.insert("", tk.END, values=(row['item_id'], row['category'], row['name'], row['price']))
            cursor.close()
        except Error as e:
            messagebox.showerror("Error fetching menu", str(e))
            
    def on_menu_select(self, event):
        selected = self.menu_tree.selection()
        if not selected:
            return
        item = self.menu_tree.item(selected[0])['values']
        category = item[1]
        name = item[2]
        
        # update description
        self.desc_label.config(text=name)
        
        # update image
        photo = self.get_image_for_category(category)
        if photo:
            self.img_label.config(image=photo, text="")
        else:
            self.img_label.config(image="", text=f"No image for {category}")

    def add_to_cart(self):
        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an item from the menu.")
            return

        item = self.menu_tree.item(selected[0])['values']
        item_id = item[0]
        name = item[2]
        price = float(item[3])
        qty = self.qty_var.get()
        
        if qty <= 0:
            messagebox.showwarning("Quantity Error", "Quantity must be at least 1.")
            return

        if item_id in self.cart_items:
            # Update quantity
            self.cart_items[item_id]['quantity'] += qty
            self.cart_items[item_id]['subtotal'] = self.cart_items[item_id]['quantity'] * price
        else:
            # Add new
            self.cart_items[item_id] = {
                'name': name,
                'price': price,
                'quantity': qty,
                'subtotal': price * qty
            }
            
        self.refresh_cart()
        
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            return
            
        item = self.cart_tree.item(selected[0])['values']
        item_id = item[0]
        
        if item_id in self.cart_items:
            del self.cart_items[item_id]
            
        self.refresh_cart()

    def refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        total = 0.0
        for item_id, details in self.cart_items.items():
            self.cart_tree.insert("", tk.END, values=(item_id, details['name'], details['quantity'], f"{details['subtotal']:.2f}"))
            total += details['subtotal']
            
        self.total_lbl.config(text=f"Total: ₹{total:.2f}")
        
    def place_order(self):
        if not self.cart_items:
            messagebox.showwarning("Cart Empty", "Your cart is empty!")
            return
            
        customer_name = self.customer_name_var.get().strip()
        if not customer_name:
            messagebox.showwarning("Customer Name", "Please enter customer name.")
            return

        total_amount = sum(item['subtotal'] for item in self.cart_items.values())
        
        try:
            cursor = self.connection.cursor()
            # 1. Insert into orders table
            insert_order_query = "INSERT INTO orders (customer_name, total_amount) VALUES (%s, %s)"
            cursor.execute(insert_order_query, (customer_name, total_amount))
            order_id = cursor.lastrowid
            
            # 2. Insert into order_items table
            insert_item_query = "INSERT INTO order_items (order_id, item_id, quantity, subtotal) VALUES (%s, %s, %s, %s)"
            order_items_data = [
                (order_id, item_id, details['quantity'], details['subtotal'])
                for item_id, details in self.cart_items.items()
            ]
            cursor.executemany(insert_item_query, order_items_data)
            
            self.connection.commit()
            cursor.close()
            
            # Show success and clear
            messagebox.showinfo("Order Placed", f"Order successfully placed for {customer_name}!\nOrder ID: {order_id}\nTotal: ₹{total_amount:.2f}")
            self.cart_items.clear()
            self.refresh_cart()
            self.customer_name_var.set("")
            self.qty_var.set(1)
            
        except Error as e:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to place order: {e}")

    # -------- Add Product Feature --------
    def open_add_product_window(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Product")
        top.geometry("300x250")
        top.configure(bg="white")
        top.grab_set() # focuses on this window
        
        tk.Label(top, text="Add Product to Menu", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
        
        form_frame = tk.Frame(top, bg="white")
        form_frame.pack(pady=5)
        
        tk.Label(form_frame, text="Category:", bg="white").grid(row=0, column=0, sticky="e", pady=5)
        cat_var = tk.StringVar(value="Pizza")
        cats = ["Pizza", "Burger", "Pasta", "Beverages", "Dessert", "Other"]
        ttk.Combobox(form_frame, textvariable=cat_var, values=cats, width=15).grid(row=0, column=1, padx=5)
        
        tk.Label(form_frame, text="Name:", bg="white").grid(row=1, column=0, sticky="e", pady=5)
        name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=name_var, width=18).grid(row=1, column=1, padx=5)
        
        tk.Label(form_frame, text="Price (₹):", bg="white").grid(row=2, column=0, sticky="e", pady=5)
        price_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=price_var, width=18).grid(row=2, column=1, padx=5)
        
        def save_product():
            cat = cat_var.get().strip()
            name = name_var.get().strip()
            price_str = price_var.get().strip()
            
            if not name or not price_str:
                messagebox.showerror("Error", "Please fill all fields.", parent=top)
                return
            try:
                price = float(price_str)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number.", parent=top)
                return
                
            try:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO menu (category, name, price) VALUES (%s, %s, %s)", (cat, name, price))
                self.connection.commit()
                cursor.close()
                messagebox.showinfo("Success", f"{name} added to menu!", parent=top)
                self.load_menu() # refresh
                top.destroy()
            except Error as e:
                messagebox.showerror("Database error", str(e), parent=top)
                
        tk.Button(top, text="Save Product", command=save_product, bg="green", fg="black", font=("Helvetica", 11)).pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniZomatoApp(root)
    root.mainloop()
