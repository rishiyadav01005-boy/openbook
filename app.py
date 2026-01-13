# UPDATED VERSION 
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

BOOK_CATEGORIES = {
    "Self Help": [
        "atomic habit.pdf",
        "mindset.pdf",
        "the psychology of money.pdf",
        "rich dad and poor dad.pdf",
        "The Millionaire Next Door.pdf"
    ],
    "Spiritual": [
        "bhagvat gita.pdf",
        "the power of now.pdf",
        "meditation for beginners.pdf",
        "ikigai.pdf"
    ],
    "Programming": [
        "Eloquent JavaScript.pdf",
        "Learning Python.pdf",
        "artificial intelligence basics.pdf",
        "let us c.pdf"
    ],
    "Fiction": [
        "harry potter.pdf",
        "The alchemist.pdf",
        "orwell1984.pdf"
    ],
    "Poetry": [
        "Milk and honey.pdf",
        "the sun and her flowers.pdf",
        "rumi.pdf"
    ]
}

# =========================
# DATABASE CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
BOOKS_DIR = os.path.join(BASE_DIR, "books")

def get_db():
    return sqlite3.connect(DB_PATH)

# =========================
# INIT DB
# =========================
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =========================
# ROUTES
# =========================

# ---------- HOME (PUBLIC) ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Email already registered!"

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user"] = user[1]   # username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid email or password!"

    return render_template("login.html")

# ---------- DASHBOARD (PROTECTED) ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user=session["user"],
        categories=BOOK_CATEGORIES
    )


# ---------- READ BOOK (PROTECTED) ----------
@app.route("/book/<filename>")
def read_book(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    return send_from_directory(BOOKS_DIR, filename)

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




