import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="prathamesh",
    password="1234",
    database="food_db"
)

cursor = conn.cursor()

print("Connected to MySQL ✅")

def get_menu():
    cursor.execute("SELECT * FROM menu")
    return cursor.fetchall()
    menu = get_menu()

    for item in menu:
        print(item)