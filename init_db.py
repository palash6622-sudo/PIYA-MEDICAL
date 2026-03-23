import sqlite3

db = sqlite3.connect("database.db")

db.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, name TEXT, product_id INTEGER)")

db.execute("INSERT INTO products (name) VALUES ('Paracetamol')")
db.execute("INSERT INTO products (name) VALUES ('Vitamin C')")
db.execute("INSERT INTO products (name) VALUES ('Cough Syrup')")

db.commit()
print("Database Created!")
