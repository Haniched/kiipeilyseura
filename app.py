# flask run
from email import message
import sqlite3
from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import forum, users

app = Flask(__name__)
app.secret_key = config.secret_key
db.ensure_schema()

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    threads = forum.get_threads()
    return render_template("index.html", threads=threads)

# Thread routes

@app.route("/new_thread", methods=["POST"])
def new_thread():
    if "user_id" not in session:
        abort(403)
    title = request.form["title"]
    content = request.form["content"]
    climbing_type = request.form["climbing_type"]
    if not title or len(title) > 20:
        abort(403)
    if not content or len(content) > 5000:
        abort(403)
    if climbing_type not in ["Bouldering", "Toprope", "Lead"]:
        abort(403)
    user_id = session["user_id"]

    thread_id = forum.add_thread(title, content, user_id, climbing_type)
    return redirect("/thread/" + str(thread_id))

@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    thread = forum.get_thread(thread_id)
    if not thread:
        abort(404)
    messages = forum.get_messages(thread_id)
    return render_template("thread.html", thread=thread, messages=messages)

@app.route("/edit_thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    thread = forum.get_thread(thread_id)
    
    if not thread:
        abort(404)
    if "user_id" not in session or thread["user_id"] != session["user_id"]:
        abort(403)  
    if thread is None:
        return "Viestiä ei löytynyt", 404

    if request.method == "GET":
        return render_template("edit.html", thread=thread)

    if request.method == "POST":
        content = request.form["content"]
        climbing_type = request.form["climbing_type"]
        forum.update_thread(thread["id"], content)
        forum.update_thread_type(thread["id"], climbing_type)
        return redirect("/thread/" + str(thread["id"]))

@app.route("/remove_thread/<int:thread_id>", methods=["GET", "POST"])
def remove_thread(thread_id):
    if "user_id" not in session:
        abort(403)
    thread = forum.get_thread(thread_id)
    if not thread:
        abort(404)
    if thread["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", thread=thread)

    if request.method == "POST":
        if "continue" in request.form:
            forum.remove_thread(thread_id)
            return redirect("/")
        return redirect("/thread/" + str(thread_id))

# Message routes
@app.route("/new_message", methods=["POST"])
def new_message():
    require_login()

    if "user_id" not in session:
        return redirect("/login")

    content = request.form["content"]
    thread_id = request.form["thread_id"]
    user_id = session["user_id"]
    
    try:
        forum.add_message(content, user_id, thread_id)
    except sqlite3.IntegrityError:
        abort(403)

    return redirect("/thread/" + str(thread_id))

@app.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    message = forum.get_message(message_id)
    
    if not message:
        abort(404)
    if "user_id" not in session or message["user_id"] != session["user_id"]:
        abort(403)  
    if message is None:
        return "Viestiä ei löytynyt", 404

    if request.method == "GET":
        return render_template("edit.html", message=message)

    if request.method == "POST":
        content = request.form["content"]
        forum.update_message(message["id"], content)
        return redirect("/thread/" + str(message["thread_id"]))

@app.route("/remove_message/<int:message_id>", methods=["GET", "POST"])
def remove_message(message_id):
    if "user_id" not in session:
        abort(403)
    message = forum.get_message(message_id)
    if not message:
        abort(404)
    if message["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", message=message)

    if request.method == "POST":
        if "continue" in request.form:
            forum.remove_message(message["id"])
        return redirect("/thread/" + str(message["thread_id"]))


# User authentication routes
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
        return "VIRHE: tunnus on jo varattu <br><a href='/register'>Takaisin</a>"

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

# User profile route
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    messages = users.get_messages(user_id)
    return render_template("user.html", user=user, messages=messages)

# Search route
@app.route("/search")
def search():
    query = request.args.get("query")
    results = forum.search(query) if query else []
    return render_template("search.html", query=query, results=results)


