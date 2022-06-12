import folium, folium.plugins
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

    def setup_db(self):
        if self.accident_type is not None:
            self.db = DB().traffic_accident()[self.accident_type]
            return self
    
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

    def request_data_from_database(self):
        if self.db is not None:
            if self.year is not None:
                temp_data = self.db.find(
                    {"發生時間":{
                        "$regex": f'^{TwYearConverter().from_year(self.year).to_tw_year()}年'
                        }})
            else:
                temp_data = self.db.find({})
            self.accident_df = pd.DataFrame(list(temp_data))
            if self.accident_df.empty:
                self.accident_df = None
                self.request_data_from_url(force=True).store_data_to_database()
            return self

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
    
    def store_data_to_database(self):
        if self.accident_df is None:
            if self.db.count_documents({}) > 1:
                self.db.update_many(
                    {'_id':''},
                    {'$set':self.accident_df.to_dict('records')},
                    upsert=True
                )
            else:
                self.db.insert_many(
                    self.accident_df.to_dict('records')
                )
            return self
            
    def get_dict(self):
        return self.accident_df.to_dict('records')

    def get_map(self, filename=None):
        locations = self.accident_df[['緯度', '經度']]
        locationlist = locations.values.tolist()
        map = folium.Map(location=locationlist[0], tiles='Stamen Terrain', zoom_start=11)
        marker_cluster = folium.plugins.MarkerCluster().add_to(map)
        for point in range(0, len(locations)-1):
            folium.Marker(
                locationlist[point], popup=folium.Popup(
                    self.accident_df['發生時間'][point]+"<br>"+self.accident_df['死亡受傷人數'][point], 
                    max_width=400), 
                icon=folium.Icon(color='darkblue', icon_color='white', 
                icon='male', angle=0, prefix='fa')).add_to(marker_cluster)
        if filename is not None:
            map.save(f"static/{filename}-map.html")
        return map