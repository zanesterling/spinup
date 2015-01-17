from flask import Flask
from pymongo import MongoClient
import urllib2

app = Flask(__name__)
db = MongoClient().loadBalancer

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	nextServer = getNextServer()
	childToCall = str(nextServer) + '/' + path

	# if there are no child servers, say so
	if not nextServer:
		return "There are no child servers at this route"

	return childToCall
	# forward request to child server
	# return result of forward

# returns next server to be forwarded to
def getNextServer():
	servers = [server for server in  db.servers.find()]

	# get next server
	serverIndex = db.config.find_one()['serverIndex']
	nextServer = None
	if len(servers) > 0:
		nextServer = servers[serverIndex % len(servers)]['url']

		# increment serverIndex in the db
		db.config.update({}, {'serverIndex': (serverIndex + 1) % len(servers)}) 

	# send back the server
	return nextServer

if __name__ == '__main__':
	app.run('0.0.0.0', 9002, debug=True)
