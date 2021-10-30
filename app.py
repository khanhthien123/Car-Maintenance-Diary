from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from helpers import *
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect("cmd.db", check_same_thread=False)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#By doing this, when executing a SELECT statement, cursor will return a list of dictionaries
#With key is the column's title, value is the value
db.row_factory = dict_factory
cursor = db.cursor()
#Display a report showing: all history maintenance in chronically
@app.route("/")
@login_required
def index():
    #all_info is a dictionary with key is car name, value is a list of dictionaries with key is column's name, value is its value
    all_info = {}
    #all_cars is a dictionary with key is car_id, value is car's name
    all_cars = get_cars(session["user_name"])
    #cars_total is a dictionary with key is the car name, value is the total cost spent
    cars_total = {}
    for car in all_cars:
        #car_info is a list of dictionaries with key is the column's name, value is its value
        car_info = cursor.execute("SELECT * FROM history WHERE user_id=? AND car_id=?", (session["user_name"], car)).fetchall()
        car_info.sort(key=lambda symbol: datetime.strptime(symbol["date"], "%Y-%m-%d"))
        total = 0
        for dic in car_info:
            total = total + dic["cost"]
        all_info[all_cars[car]] = car_info
        cars_total[all_cars[car]] = total

    return render_template("index.html", all_info=all_info, cars_total=cars_total)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    #get user_name from the register form
    user_name = request.form.get("user_name")

    #check if the id exists
    all_id = cursor.execute("SELECT * FROM users WHERE user_name=?", (user_name,))
    if len(all_id.fetchall()) > 0:
        return apology("This user name already exists")
    
    password = request.form.get("password")
    pass_confirm = request.form.get("password_confirmation")
    if password != pass_confirm:
        return apology("Password and Confirmation doesn't match")
    
    pass_hash = generate_password_hash(password)
    cursor.execute("INSERT INTO users (user_name, hash) VALUES (?, ?)", (user_name, pass_hash))
    db.commit()
    return redirect("/login")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    user_name = request.form.get("user_name")

    #check if entered user_name is valid
    user_list = cursor.execute("SELECT * FROM users WHERE user_name=?", (user_name,))
    data = user_list.fetchall()
    if len(data) != 1:
        return apology("Invalid ID")
    
    
    password = request.form.get("password")
    checking = check_password_hash(data[0]["hash"], password)

    if not checking:
        return apology("Wrong password")

    session["user_name"] = user_name
    return redirect("/")



#Add a car. A car needs a brand, year, current mileague
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    types = ["SUV", "Sedan", "Truck", "Trailer"]
    if request.method == "GET":
        return render_template("add.html", types=types, data=data)

    #will add input validation later
    brand = request.form.get("brand")
    year = request.form.get("year")
    car_type = request.form.get("type")
    car_id = session["user_name"] + brand + year + car_type

    print(brand, car_id, year, car_type)

    cursor.execute("INSERT INTO cars (user_id, brand, year, type, car_id) VALUES (?, ?, ?, ?, ?)", (session["user_name"], brand, year, car_type, car_id))
    db.commit()
    return redirect("/add")

#return a dictionary with key is the car_id, value is the name of the car
def get_cars(user_name):
    #should return a dictionary
    printed_cars = {}
    data = cursor.execute("SELECT * FROM cars WHERE user_id=?", (user_name,)).fetchall()
    for i in data:
        name = i["brand"] + " " + str(i["year"]) + " " + i["type"]
        printed_cars[i["car_id"]] = name

    return printed_cars

@app.route("/maintain", methods=["GET", "POST"])
@login_required
def maintain():
    #Get all user's cars
    printed_cars = get_cars(session["user_name"])
    if request.method == "GET":
        return render_template("maintenance.html", fixing=fixing, printed_cars=printed_cars, parts=parts)
    date = request.form.get("date")
    #car is the car_id
    car = request.form.get("car")
    #Get car_id from car
    part = request.form.get("part")
    service = request.form.get("maintain")
    money = request.form.get("money")
    place = request.form.get("where")
    note = request.form.get("note")
    mileague = request.form.get("mileague")
    cursor.execute("INSERT INTO history (user_id, car_id, part, service, place, cost, note, date, mileague) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
     (session["user_name"], car, part, service, place, money, note, date, mileague))

    db.commit()
    return redirect("/maintain")