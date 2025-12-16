from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

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

app.run(debug=True)