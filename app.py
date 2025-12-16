import sqlite3
import os

def init_db():
    if not os.path.exists("quiz.db"):
        conn = sqlite3.connect("quiz.db")
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            answer TEXT
        )
        """)

        conn.commit()
        conn.close()

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

app = Flask(__name__)
app.secret_key = "quizsecret"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = cur.fetchone()

        if result:
            session["user"] = user
            return redirect("/quiz")
    return render_template("login.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()

    if request.method == "POST":
        score = 0
        for q in questions:
            if request.form.get(str(q[0])) == q[5]:
                score += 1
        return render_template("result.html", score=score)

    return render_template("quiz.html", questions=questions)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)