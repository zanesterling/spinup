import pymongo 
from pymongo import MongoClient 

client = MongoClient()
db = client.spinup 

db.drop_collection("data")

