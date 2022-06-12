import pymongo

class DB:
    _db = None 
    client = None

    def __new__(cls, *args, **kwargs): 
        if cls._db is None: 
            cls._db = super().__new__(cls) 
        return cls._db 

    def __init__(self, host=None):
        self.set_host(host)
    
    def set_host(self, host=None):
        if host is not None:
            self.client = pymongo.MongoClient(host)

    def traffic_accident(self):
        return self.client.traffic_accident