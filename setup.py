import os
from datetime import date
from app.db import DB
from app.traffic_accident import TrafficAccident

db = DB(os.environ.get('DB_URL'))

ta1 = TrafficAccident(year=date.today().year, accident_type='A1')
ta1.request_data_from_url().store_data_to_database()
ta2 = TrafficAccident(year=date.today().year, accident_type='A2')
ta2.request_data_from_url().store_data_to_database()