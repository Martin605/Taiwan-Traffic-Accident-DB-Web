import pandas as pd
from datetime import date
from app.converter import TwYearConverter
from app.db import DB

class TrafficAccident():
    
    year = None
    accident_type = None
    url = None

    accident_df = None
    db = None

    def __init__(self, year=None, accident_type=None, url=[]):
        self.url = url
        self.setup(year, accident_type)
        self.setup_db()
        if self.year is not None and self.accident_type is not None:
            self.request_data_from_database()

    # set collection
    def setup_db(self):
        if self.accident_type is not None:
            self.db = DB().traffic_accident()[self.accident_type]
            return self
    
    # set info and url
    def setup(self, year=None, accident_type=None):
        if (year is not None) or (self.year is None):
            if isinstance(year, str):
                year = eval(year)
            self.year = year
        if (accident_type is not None) or (self.accident_type is None):
            self.accident_type = accident_type
        if (self.year is not None) and (self.accident_type is not None):
            if self.year == date.today().year:
                if self.accident_type == "A1":
                    self.url = ["https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=BF1377E4-73DE-4DD1-9C2F-174E28EA1031"]
                elif self.accident_type == "A2":
                    self.url = ["https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=219560DB-5617-4C5F-9754-8A4B96AC5F42"]
                elif self.accident_type == "A3":
                    self.url = ["https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=6EC4380A-0F8A-4D68-809B-2218930F08FB"]

    # get data from db
    def request_data_from_database(self):
        if self.db is not None:
            if self.year is not None:
                temp_data = self.db.find(
                    {"發生時間":{
                        "$regex": f'^{TwYearConverter().from_year(self.year).to_tw_year()}年'
                        }},{"_id":0})
            else:
                temp_data = self.db.find({},{"_id":0})
            self.accident_df = pd.DataFrame(list(temp_data))
            if self.accident_df.empty:
                self.accident_df = None
                return self.request_data_from_url(force=True).store_data_to_database()
            return self

    # get data from url
    def request_data_from_url(self, force=False):
        if force or (self.accident_df is None) :
            for url in self.url:
                temp_data = pd.read_csv(url)
                temp_data.drop(temp_data.tail(2).index, inplace=True)
                if self.accident_df is None:
                    self.accident_df = temp_data
                else:
                    self.accident_df = self.accident_df.append(temp_data, ignore_index=True)
        return self
    
    # store data to database
    def store_data_to_database(self):
        if self.db is not None:
            dbcount = self.db.count_documents({})
            if dbcount > 1:
                self.db.insert_many(
                    self.accident_df.iloc[dbcount-1:].to_dict('records')
                )
            else:
                self.db.insert_many(
                    self.accident_df.to_dict('records')
                )
            return self

    def get_dict(self):
        return self.accident_df.to_dict()

    def get_dict_records(self):
        return self.accident_df.to_dict('records')

# get data from url and store into database
def update_data():
    ta1 = TrafficAccident(year=date.today().year, accident_type='A1')
    ta1.request_data_from_url().store_data_to_database()
    ta2 = TrafficAccident(year=date.today().year, accident_type='A2')
    ta2.request_data_from_url().store_data_to_database()