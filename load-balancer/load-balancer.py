from flask import Flask, request
from pymongo import MongoClient
from urllib2 import urlopen

app = Flask(__name__)
db = MongoClient().loadBalancer

@app.route('/service', methods=['POST'])
def service():
	data = request.form

	if data['type'] == 'add-server':
		# add a server to the stored list
		server = {'url': data['url']}
		db.servers.insert(server)
		return 'success'
	elif data['type'] == 'rmv-server':
		# remove a server from the stored list
		server = {'url': data['url']}
		db.servers.remove(server)
		return 'success'

	return 'command not supported: ' + data['type']

# note: only does GET requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>') # catch-all path
def catch_all(path):
	nextServer = getNextServer()
	# if there are no child servers, say so
	if not nextServer:
		return "There are no child servers at this route"

	# forward request to child server
	childToCall = str(nextServer) + '/' + path
	print childToCall
	response = urlopen(childToCall)

	# return result of forward
	return response.read() + '<br>brought to you by:' + childToCall

# returns next server to be forwarded to
def getNextServer():
	servers = [server for server in db.servers.find()]

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
