import os
from app.db import DB
from app.traffic_accident import  update_data

db = DB(os.environ.get('DB_URL'))
update_data()