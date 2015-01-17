from flask import Flask, session, request, session,  render_template
from pymongo import MongoClient
import requests
from models import users, data
import json

app = Flask(__name__)
db = MongoClient().spinup
app.secret_key = "herro"

CLIENT_ID = 'bb93565e1f2db84beeb740a0d704d820fb93f1a5db4984050b23121dfe583a7b'
CLIENT_SECRET = 'e0fba3d9cf155f3cef4ae275e7abb3c05fb5c157260beec55a15ef2acc88bec9'
CALLBACK = 'http://104.131.75.88:9001/callback'

# webpage and ui
@app.route('/')
def home():
    d = {}
    if not 'username' in session:
        d['logged_in'] = False
        return render_template("login.html", d=d)
    
    if 'username' in session and not User.user_exists(session['username']):
        return render_template("login.html", d=d)

    d['logged_in'] = True
    d['username'] = session['username']
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
    r = requests.post(url).text
    response_dict = json.loads(response)
    if 'access_token' in response_dict:
        session['username'] = response_dict["info"]["name"]
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
