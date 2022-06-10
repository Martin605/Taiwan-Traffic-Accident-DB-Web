import pymongo

class DB:
    _db = None 
    client = None

    def __new__(cls, *args, **kwargs): 
        if cls._db is None: 
            cls._db = super().__new__(cls) 
        return cls._db 

    def __init__(self, host="mongodb://localhost:27017/"):
        if self.client is None:
            self.client = pymongo.MongoClient(host)

    def test(self):
        return self.client.students