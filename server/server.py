from flask import Flask, session, request, render_template
from pymongo import MongoClient
import requests

app = Flask(__name__)
db = MongoClient().spinup
CLIENT_ID = 'bb93565e1f2db84beeb740a0d704d820fb93f1a5db4984050b23121dfe583a7b'
CLIENT_SECRET = 'e0fba3d9cf155f3cef4ae275e7abb3c05fb5c157260beec55a15ef2acc88bec9'
CALLBACK = 'http://104.131.75.88:9001/callback'

# webpage and ui
@app.route('/')
def home():
	d = {'signed_in': False} # TODO
	return render_template('home.html', d=d)

@app.route('/callback', methods=['GET', 'POST'])
def authenticate():
    code = request.args['code']
    url =   ("https://cloud.digitalocean.com/v1/oauth/token"
    "?client_id=%(client_id)s"
    "&client_secret=%(client_secret)s" 
    "&code=%(code)s&"
    "grant_type=authorization_code&"
    "redirect_uri=%(callback_URL)s") %{'client_id': CLIENT_ID, "client_secret": CLIENT_SECRET,
                                              "code":code,
                                              "callback_URL": CALLBACK}
    r = requests.post(url)
    return r.text

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
