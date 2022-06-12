import os
from datetime import date
from flask import Flask, render_template
from app.db import DB
from app.traffic_accident import TrafficAccident


app = Flask(__name__)
db = DB(os.environ.get('DB_URL'))

@app.route("/")
@app.route("/index")
def index():
    return TrafficAccident(year=date.today().year, accident_type='A1').get_map()._repr_html_()

@app.route("/TrafficAccidentMap/<year>/<accident_type>")
def trafficAccidentMap(year, accident_type):
    return str(TrafficAccident(year=year, accident_type=accident_type).get_dict())

app.run()