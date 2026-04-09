# 🍔 Food Order Management System (Mini Zomato)

## 📌 Project Overview

The **Food Order Management System** is a desktop-based application developed using Python and MySQL. It allows users to view a menu, select food items, place orders, and generate bills through a simple graphical user interface.

This project demonstrates the integration of a database with a Python application and provides a basic simulation of an online food ordering system like Zomato.

---

## 🚀 Features

* 📋 Display food menu from database
* 🛒 Place food orders with quantity
* 💾 Store orders in MySQL database
* 🧾 Generate bill automatically
* 🎨 Simple GUI using Tkinter
* 🖼 Food images display
* ⚠️ Error handling (invalid input, no selection)

---

## 🛠️ Tech Stack

* **Frontend (GUI):** Tkinter (Python)
* **Backend (Database):** MySQL
* **Programming Language:** Python
* **Libraries Used:**

  * mysql-connector-python
  * tkinter
  * pillow (for images)

---

## 📂 Project Structure

```
Mini_Zomato_Project/
│
├── assets/
│   ├── Burger.png
│   ├── Pizza.png
│   ├── Pasta.png
│   ├── Dessert.png
│   ├── Beverages.png
│   └── Other.png
│
├── venv/
├── app.py
├── db_setup.py
├── requirements.txt
├── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/FoodOrderSystem.git
cd FoodOrderSystem
```

---

### 2️⃣ Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```
python3 -m pip install mysql-connector-python pillow
```

---

### 4️⃣ Setup MySQL Database

Run the following SQL commands:

```sql
CREATE DATABASE food_db;
USE food_db;

CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    price INT
);

INSERT INTO menu (name, price) VALUES
('Burger', 120),
('Pizza', 250),
('Pasta', 180),
('Sandwich', 100);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(50),
    quantity INT,
    total_price INT
);

CREATE USER 'prathamesh'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON food_db.* TO 'prathamesh'@'localhost';
FLUSH PRIVILEGES;
```

---

### 5️⃣ Run the Application

```
python3 main.py
```

---

## 📸 Screenshots

* Menu display
* Order placement
* Bill generation popup

*(You can add screenshots here)*

---

## 🧠 Concepts Used

* Database connectivity in Python
* CRUD operations (Create, Read)
* GUI development with Tkinter
* Event-driven programming

---

## ⚠️ Notes

* Ensure MySQL server is running before starting the app
* Image files must be in the same folder as `main.py`
* Database credentials should match your local setup

---

## 🔮 Future Enhancements

* 🛒 Add cart system
* 🔐 User login authentication
* 🌐 Convert to web app using Flask
* 📊 Sales analytics dashboard
* 🎨 Advanced UI design

---

## 👨‍💻 Author

**Pratham Kun**

---

## 📜 License

This project is for educational purposes.
