# flask run
from flask import Flask
from flask import redirect, render_template, request
import db

app = Flask(__name__)

@app.route("/")
def index():
    messages = db.query("SELECT content FROM messages")
    count = len(messages)
    return render_template("index.html", count=count, messages=messages)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]    
    db.execute("INSERT INTO messages (content) VALUES (?)", [content])
    return redirect("/")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/result", methods=["POST"])
def result():
    option = request.form["option"]
    types = request.form.getlist("type")
    message = request.form["message"]
    return render_template("result.html", option=option, types=types, message=message)
