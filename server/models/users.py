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
        
        person = db.users.find_one({"name": self.name})
        
        if person:
            User.update_user(self.name, self.access_token)
        else:
            db.users.insert(doc)

    @staticmethod
    def update_user(username, access_token):
        db.users.update({'username': username}, {'$set': {'access_token': access_token}})

    @staticmethod
    def get(name): 
        return db.users.find_one({"name":name})

    @staticmethod
    def user_exists(name):
        if User.get(name) != None:
            return True
        else:
            return False
