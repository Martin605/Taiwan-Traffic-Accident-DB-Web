import os, json 
from datetime import date
from flask import Flask, render_template
from app.db import DB
from app.traffic_accident import TrafficAccident, update_data


app = Flask(__name__)
db = DB(os.environ.get('DB_URL'))

# return index page
@app.route("/")
@app.route("/index")
def index():
    year=date.today().year
    return render_template("index.html",year=year,accident_type="A1")

# return Traffic Accident Page
@app.route("/TrafficAccident/<year>/<accident_type>")
def trafficAccident(year, accident_type):
    if year == "now":
        year=date.today().year
    return render_template("index.html",year=year,accident_type=accident_type)

# return Traffic Accident Data
@app.route("/TrafficAccidentData/<year>/<accident_type>")
def trafficAccidentData(year, accident_type='A1'):
    if year == "now":
        year=date.today().year
    return json.dumps(TrafficAccident(year=year, accident_type=accident_type).get_dict())

# update data from gov
@app.route("/TrafficAccidentDataUpdate")
def trafficAccidentDataUpdate():
    update_data()
    return "200"
    
app.run()