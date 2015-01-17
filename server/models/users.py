from pymongo import MongoClient
import pymongo
from datetime import datetime
import hashlib

client  = MongoClient()
db = client.spinup 

class User(): 
    def __init__(self, access_token, name): 
        self.access_token = access_token
        self.name = name
        self.spinup_api = hashlib.sha256(self.name).hexdigest() 
    
    def put(self):
        doc = {"access_token": self.access_token,
                "name": self.name,
                "spinup_api_key": self.spinup_api,
                "loadmanager": None, 
                "child_droplet": None}
        
        person = db.users.find_one({"name": self.name})
        
        if person:
            User.update_user(self.name, self.access_token)
        else:
            db.users.insert(doc)

    @staticmethod
    def get_child_droplet(name):
        user = db.users.find_one({'name': name})
        if 'child_droplet' in user:
            return user['child_droplet']
        return None

    @staticmethod
    def get_loadmanager(name):
        user = db.users.find_one({'name': name})
        if 'loadmanager' in user:
            return user['loadmanager']
        return None
    
    @staticmethod
    def add_child_droplet(name, child):
        db.users.update({'name': name}, {'$set': {'child_droplet':child}})
    
    @staticmethod
    def add_loadmanager(name, loadmanager):
        db.users.update({'name': name}, {'$set': {'loadmanager':loadmanager}})

    @staticmethod
    def get_api_key(username): 
        user = db.users.find_one({"name":username})
        if 'spinup_api_key' in user:
            return user['spinup_api_key']
        else:
            api_key = hashlib.sha256(username).hexdigest()
            db.users.update({'name': username}, {'spinup_api_key': api_key})
            return api_key

    @staticmethod
    def update_user(username, access_token):
        db.users.update({'name': username}, {'$set': {'access_token': access_token}})

    @staticmethod
    def get(name): 
        return db.users.find_one({"name":name})

    @staticmethod
    def user_exists(name):
        if User.get(name) != None:
            return True
        else:
            return False
