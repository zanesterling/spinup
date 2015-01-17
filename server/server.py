from flask import Flask, url_for, redirect,  session, request, session,  render_template
from pymongo import MongoClient
import requests
from models.users import User
from models.data import Data
import json

import secrets

app = Flask(__name__)
db = MongoClient().spinup
app.secret_key = "herro"

# webpage and ui
@app.route('/')
def home():
    d = {}
    if not 'username' in session or not User.user_exists(session['username']):
        d['signed_in'] = False
        d['client_id'] = secrets.CLIENT_ID
        d['callback_url'] = secrets.CALLBACK
        print d
        return render_template("login.html", d=d)

    d['signed_in'] = True
    d['username'] = session['username']
    d['api_key'] = User.get_api_key(d['username'])
    url = "https://cloud.digitalocean.com/v2/droplets" 
    headers = {"Authorization": "Bearer " + session["access_token"]} 
    droplets = request.post(url, headers).text
    print droplets
    return render_template('home.html', d=d)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
    

@app.route('/callback', methods=['GET', 'POST'])
def oauth_callback():
    code = request.args['code']
    url =   ("https://cloud.digitalocean.com/v1/oauth/token"
    "?client_id=%(client_id)s"
    "&client_secret=%(client_secret)s" 
    "&code=%(code)s&"
    "grant_type=authorization_code&"
    "redirect_uri=%(callback_URL)s") %{'client_id': secrets.CLIENT_ID, "client_secret": secrets.CLIENT_SECRET,
                                              "code":code,
                                              "callback_URL": secrets.CALLBACK}
    r = requests.post(url).text
    response_dict = json.loads(r)
    if 'access_token' in response_dict:
        session['access_token'] = response_dict['access_token']
        session['username'] = response_dict["info"]["name"]
        new_user = User(access_token = session['access_token'], name=session['username']) 
        print session['access_token']
        new_user.put()
    return redirect(url_for('home')) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # POST
    return 'you poster bro'

# daemon interaction
@app.route('/payload', methods=['POST'])
def service():
    data = request.data
    api = None
    if 'X-spinup-api' in request.headers:
        api = request.headers['X-spinup-api']
    else: 
        return 

    jdata = json.loads(data)
    for piece in jdata:
        new_data = Data(
                timestamp=piece['timestamp'],
                payload = piece['data'],
                api_key = api)
        new_data.put()
    return 'OK'

@app.route('/stats', methods=['POST'])
def stats():
    return render_template('stats.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 9001, debug=True)
