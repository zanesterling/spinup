from pymongo import MongoClient
import pymongo
from datetime import datetime


client  = MongoClient()
db = client.spinup 

class User(): 
    def __init__(self, access_token, name): 
        self.access_token = access_token
        self.name = name 
    
    def put(self):
        doc = {"access_token": self.access_token,
                "name": self.name}
        
        people = db.users.find({"name": self.name})
        
        for person in people:
            db.users.remove(person['_id']) 
        
        db.users.insert(doc)

    @staticmethod
    def get(name): 
        search_specs = {"name": name}
        return db.users.find_one({spec: search_specs})

    @staticmethod
    def user_exists(name):
        if User.get(name) != None:
            return True
        else:
            return False
