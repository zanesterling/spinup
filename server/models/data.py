from pymongo import MongoClient
import pymongo
from datetime import datetime

#initialize the client
client = MongoClient()
db = client.spinup

class Data():
    def __init__(self, timestamp, payload, api_key, datatype=None):
        self.payload = payload
        self.datatype = datatype
        self.timestamp = datetime.strptime(timestamp, "%m:%d:%y:%H:%M:%S")
        self.api_key = api_key

    def put(self):
        doc = {"datatype": self.datatype,
               "timestamp": self.timestamp,
               "api_key":self.api_key 
               }
        for key in self.payload:
            if not key in doc:
                doc[key] = self.payload[key]
            else:
                raise KeyError("Duplicate keys!")
        
        db.data.insert(doc)
    
    @staticmethod
    def get(api_key, number = None):
        search_specs = {"api_key": api_key}
        return db.data.find(spec = search_specs).sort("timestamp", pymongo.DESCENDING )
        

if __name__ == "__main__":
    p = {"event1": [(1, 10), (2, 12), (3, 8)]}
    datapoint = Data(payload = p, timestamp = datetime.now().strftime("%m:%d:%y:%H:%M:%S"))
    datapoint.put()

    cursor = Data.get(uid="123456789")

