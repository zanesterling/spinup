from flask import Flask, url_for, redirect,  session, request, session,  render_template
from pymongo import MongoClient
import requests
import json
import digitalocean
from random import random
import time

from models.users import User
from models.data import Data
import secrets
import setup

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
    d['childserver'] = None

    if 'childserver' in session:
        d['childserver'] = session['childserver']
    
    # get dict of droplets on this account
    manager = digitalocean.Manager(token=session["access_token"])
    my_droplets = manager.get_all_droplets()
    droplet_dict = {}
    for droplet in my_droplets:
        droplet_dict[droplet.name] = droplet.id
    d['droplets'] = droplet_dict

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

#redirects to child droplet configuration page
@app.route('/configure', methods=['GET']) 
def configure_droplet():
    d = {}
    if not 'username' in session or not User.user_exists(session['username']):
        d['signed_in'] = False
        d['client_id'] = secrets.CLIENT_ID
        d['callback_url'] = secrets.CALLBACK
        print d
        return render_template("login.html", d=d)
    d['signed_in'] = True
    d['username'] = session['username']
    d['droplet'] = request.args['droplet']
    d['dropletname'] = request.args['name']
    return render_template('configure.html', d=d)


#takes a snapshot of the server.
@app.route('/snapshot', methods=['GET'])
def snapshot():
    servername = request.args['dropletname']
    session['childserver'] = servername

    manager = digitalocean.Manager(token=session["access_token"])
    my_droplets = manager.get_all_droplets()
    my_images = manager.get_all_images() 
    for image in my_images:
        if image.name == 'SPINUP':
            image.destroy()

    for droplet in my_droplets:
        if droplet.name == servername:
            droplet.shutdown()
            stall = True
            while stall:
                droplet.load()
                if droplet.status == 'off':
                    stall = False
                time.sleep(1)
            droplet.take_snapshot(snapshot_name="SPINUP")
    return redirect(url_for('home')) 

@app.route('/install/<api_key>')
def install(api_key):
    return setup.get_file(api_key)

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

@app.route('/stats')
def stats():
    if not 'username' in session:
        return redirect(url_for('home'))

    d = {}
    d['logged_in'] = ('username' in session)

    # randomly generate a debug dataset
    d['datasets'] = []
    for j in range(3):
        dataset = {'key': 'Datafeed name'}
        dataset['data'] = []
        for i in range(25):
            dataset['data'].append(random() * 100)
        d['datasets'].append(dataset)
    return render_template('stats.html', d=d)

if __name__ == '__main__':
    app.run('0.0.0.0', 9001, debug=True)
