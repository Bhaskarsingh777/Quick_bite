from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

# Create Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_NAME = "fooddb.sqlite"

# ---------- Ensure Database and Tables ----------
con = sqlite3.connect(DB_NAME)
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    name TEXT,
    quantity INTEGER,
    address TEXT,
    phone TEXT,
    status TEXT DEFAULT 'Preparing'
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message TEXT,
    rating INTEGER
)
""")

con.commit()
con.close()


# ---------- HOME ----------
@app.route("/")
def home():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT name, message, rating FROM reviews ORDER BY id DESC")
    reviews = cur.fetchall()
    con.close()
    return render_template("index.html", reviews=reviews)


# ---------- SIGNUP ----------
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                    (name, email, password))
        con.commit()
        flash("Signup successful! Please login.")
    except:
        flash("Email already exists!")
    con.close()

    return redirect(url_for("home"))


# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()
    con.close()

    if user:
        session["user"] = email
        flash("Login Successful!")
    else:
        flash("Invalid Login!")
    return redirect(url_for("home"))


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out!")
    return redirect(url_for("home"))


# ---------- ORDER ----------
@app.route("/order", methods=["POST"])
def order():
    if "user" not in session:
        flash("Login required!")
        return redirect(url_for("home"))

    item = request.form["item"]
    email = session["user"]
    quantity = request.form["quantity"]
    address = request.form["address"]
    phone = request.form["phone"]

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT INTO orders(item, name, quantity, address, phone) VALUES (?, ?, ?, ?, ?)",
            (item, email, quantity, address, phone))
    con.commit()
    con.close()

    flash("Order placed successfully!")
    return redirect(url_for("home"))


# ---------- SAVE REVIEW ----------
@app.route("/review", methods=["POST"])
def review():
    name = request.form["name"]
    message = request.form["message"]
    rating = request.form["rating"]

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT INTO reviews(name, message, rating) VALUES (?, ?, ?)", 
                (name, message, rating))
    con.commit()
    con.close()

    flash("Feedback submitted! 👍")
    return redirect(url_for("home"))


# ---------- TRACK ORDERS (User Only) ----------
@app.route("/track_orders")
def track_orders():
    if "user" not in session:
        flash("Login to track order")
        return redirect(url_for("home"))

    email = session["user"]
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM orders WHERE name=? ORDER BY id DESC", (email,))

    orders = cur.fetchall()
    con.close()

    return render_template("track_orders.html", orders=orders)


# ---------- ADMIN LOGIN ----------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = "admin"
            return redirect(url_for("admin_dashboard"))
        flash("Invalid Admin Credentials!")
    return render_template("admin_login.html")


# ---------- ADMIN DASHBOARD ----------
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    con.close()

    return render_template("admin_dashboard.html", users=users, orders=orders)


# ---------- UPDATE ORDER STATUS ----------
@app.route("/update_status/<int:order_id>", methods=["POST"])
def update_status(order_id):
    status = request.form["status"]

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    con.commit()
    con.close()

    flash("Order Status Updated!")
    return redirect(url_for("admin_dashboard"))


# ---------- DELETE USER ----------
@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    con.commit()
    con.close()

    flash("User deleted successfully!")
    return redirect(url_for("admin_dashboard"))


# ---------- DELETE ORDER ----------
@app.route("/delete_order/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("DELETE FROM orders WHERE id=?", (order_id,))
    con.commit()
    con.close()

    flash("Order deleted successfully!")
    return redirect(url_for("admin_dashboard"))


# ---------- ADMIN LOGOUT ----------
@app.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    flash("Admin Logged Out!")
    return redirect(url_for("admin_login"))


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
