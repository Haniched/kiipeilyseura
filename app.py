# flask run
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import forum

app = Flask(__name__)
app.secret_key = config.secret_key
db.ensure_schema()

@app.route("/")
def index():
    threads = forum.get_threads()
    return render_template("index.html", threads=threads)

@app.route("/new_thread", methods=["POST"])
def new_thread():
    title = request.form["title"]
    content = request.form["content"]
    climbing_type = request.form["climbing_type"]
    user_id = session["user_id"]

    thread_id = forum.add_thread(title, content, user_id, climbing_type)
    return redirect("/thread/" + str(thread_id))

@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    thread = forum.get_thread(thread_id)
    messages = forum.get_messages(thread_id)
    return render_template("thread.html", thread=thread, messages=messages)

@app.route("/new_message", methods=["POST"])
def new_message():
    if "user_id" not in session:
        return redirect("/login")

    content = request.form["content"]
    thread_id = request.form["thread_id"]
    user_id = session["user_id"]

    forum.add_message(content, user_id, thread_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    message = forum.get_message(message_id)
    if message is None:
        return "Viestiä ei löytynyt", 404

    if request.method == "GET":
        return render_template("edit.html", message=message)

    if request.method == "POST":
        content = request.form["content"]
        climbing_type = request.form["climbing_type"]
        forum.update_message(message["id"], content)
        forum.update_thread_type(message["thread_id"], climbing_type)
        return redirect("/thread/" + str(message["thread_id"]))

@app.route("/remove/<int:message_id>", methods=["GET", "POST"])
def remove_message(message_id):
    message = forum.get_messages(message_id)

    if request.method == "GET":
        return render_template("remove.html", message=message)

    if request.method == "POST":
        if "continue" in request.form:
            forum.remove_message(message["id"])
        return redirect("/thread/" + str(message["thread_id"]))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat <br><a href='/'>Takaisin etusivulle</a>"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu <br><a href='/'>Takaisin etusivulle</a>"

    return "Tunnus luotu <br><a href='/'>Takaisin etusivulle</a>"   

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if not result:
        return "VIRHE: väärä tunnus tai salasana"

    user_id, password_hash = result[0]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
