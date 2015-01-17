from flask import Flask, session, request, render_template
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient().spinup

# webpage and ui
@app.route('/')
def home():
	d = {'signed_in': False} # TODO
	return render_template('home.html', d=d)

@app.route('/callback', methods=['GET', 'POST'])
def authenticate():
    return 'yo'

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')

	# POST
	return 'you poster bro'

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	# POST
	return 'you poster bro'

# daemon interaction
@app.route('/service', methods=['POST'])
def service():
	return 'accepted'

if __name__ == '__main__':
	app.run('0.0.0.0', 9001, debug=True)
