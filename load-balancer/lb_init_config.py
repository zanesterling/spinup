from pymongo import MongoClient

db = MongoClient().loadBalancer
db.config.remove()
config = {
	'serverIndex': 0
}
db.config.insert(config)
