# flask run
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    words = ["Name", "Number", "Email", "Address"]
    return render_template("index.html", message="Welcome!", items=words)

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
