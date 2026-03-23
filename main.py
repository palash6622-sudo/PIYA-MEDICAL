from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    db = sqlite3.connect("database.db")
    
    db.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, name TEXT, product_id INTEGER)")

    # default products (only if empty)
    count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        db.execute("INSERT INTO products (name) VALUES ('Paracetamol')")
        db.execute("INSERT INTO products (name) VALUES ('Vitamin C')")
        db.execute("INSERT INTO products (name) VALUES ('Cough Syrup')")

    db.commit()

init_db()
def connect_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    db = connect_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("index.html", products=products)

@app.route("/order", methods=["POST"])
def order():
    name = request.form["name"]
    product_id = request.form["product_id"]

    db = connect_db()
    db.execute("INSERT INTO orders (name, product_id) VALUES (?, ?)", (name, product_id))
    db.commit()

    return "Order Placed Successfully!"

@app.route("/admin")
def admin():
    db = connect_db()
    orders = db.execute("SELECT * FROM orders").fetchall()
    return render_template("admin.html", orders=orders)

if __name__ == "__main__":
    app.run()  
from flask import session

app.secret_key = "12345"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == "admin" and pwd == "1234":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    db = connect_db()
    orders = db.execute("SELECT * FROM orders").fetchall()
    return render_template("admin.html", orders=orders)
