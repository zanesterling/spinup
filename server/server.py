from flask import Flask, url_for, redirect,  session, request, session,  render_template
from pymongo import MongoClient
import requests
import json
import digitalocean
from random import random
import time
from datetime import datetime

from models.users import User
from models.data import Data
import secrets
import setup

app = Flask(__name__)
db = MongoClient().spinup
app.secret_key = "herro"

cur_api_key = [None]

CPU_LOAD_THRESHOLD = 40

@app.route('/easter')
def easter():
    if 'easter' in session:
        session.pop('easter')
    else:
        session['easter'] = 'E A S T E R B O Y Z'
    return redirect(url_for('home'))

# webpage and ui
@app.route('/')
def home():
    d = {}
    if not 'username' in session or not User.user_exists(session['username']):
        d['signed_in'] = False
        d['client_id'] = secrets.CLIENT_ID
        d['callback_url'] = secrets.CALLBACK
        d['easter'] = 'easter' in session
        return render_template("login.html", d=d)

    username = session['username']
    d['signed_in'] = True
    d['username'] = username
    d['api_key'] = User.get_api_key(d['username'])
    d['childserver'] = User.get_child_droplet(username)
    d['loadmanager'] = User.get_loadmanager(username)
    d['easter'] = 'easter' in session
   
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
        return render_template("login.html", d=d)
    d['signed_in'] = True
    d['username'] = session['username']
    d['droplet'] = request.args['droplet']
    d['dropletname'] = request.args['name']
    d['api_key'] = User.get_api_key(d['username'])
    d['easter'] = 'easter' in session
    return render_template('configure.html', d=d)

@app.route('/configure_loadmanager', methods=['GET'])
def configure_loadmanager(): 
    loadmanager = request.args['loadmanager']
    user = session['username']
    User.add_loadmanager(user, loadmanager)
    return redirect(url_for('home'))

#takes a snapshot of the server.
@app.route('/snapshot', methods=['GET'])
def snapshot():
    servername = request.args['dropletname']    
    user = session['username']
    User.add_child_droplet(user, servername)


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
    return setup.get_file(api_key, secrets.HOST_IP)

# daemon interaction
@app.route('/payload', methods=['POST'])
def service():
    data = request.data
    api = None
    if 'X-spinup-api' in request.headers:
        api = request.headers['X-spinup-api']
    else: 
        return 
    
    # receive and store data from payload
    jdata = json.loads(data)
    for piece in jdata:
        new_data = Data(
                timestamp=piece['timestamp'],
                payload = piece['data'],
                api_key = api)
        new_data.put()
    
    # average cpu load over last ten frames
    d = Data.get(api)
    count = d.count() 
    d = d[0:min(10, count)]
    sum_ = 0.
    for data in d:
        inc = data['cpu']
        sum_ += inc
    sum_ = sum_ * 1.0 / min(10, count)
    print sum_
    
    if sum_ > CPU_LOAD_THRESHOLD:
        print "high load: spinning up a new server"
        cur_api_key[0] = api
        return redirect(url_for('spinup'))
    return 'OK'

@app.route('/stats')
def stats():
    if not 'username' in session:
        return redirect(url_for('home'))

    d = {}
    d['logged_in'] = ('username' in session)

    # fetch dataset from the past month
    api_key = User.get_api_key(session['username'])
    last_month = datetime.now()
    last_month = last_month.replace(month=((last_month.month - 2) % 12 + 1))
    if last_month.month == 12: # if we looped a year, decrement the year
        last_month = last_month.replace(year=(last_month.year - 1))
    data = Data.get(api_key, start_time=last_month)

    # sort data into appropriate streams
    d['datasets'] = {}
    for i in range(min(data.count(), 47)):
        datum = data.next()
        for k,v in datum.items():
            # skip built-in keys
            if k in ['datatype', 'timestamp', 'api_key', '_id']:
                continue

            k = k.encode('ascii', 'ignore')
            if k not in d['datasets']:
                d['datasets'][k] = []
            d['datasets'][k].append(v)

    # stick api_key in there too
    d['api-key'] = api_key
    d['easter'] = 'easter' in session

    return render_template('stats.html', d=d)

@app.route('/spinup', methods=['GET','POST'])
def spinup():
    print "STARTING TO SPIN THE FUCK UP"
    api_key = None
    if 'username' not in session:
        if cur_api_key[0]:
            api_key = cur_api_key[0]
            cur_api_key[0] = None
        else:
            print "COULDNT FIND THE FUCKING USER FUCKING NAME FUCK" 
            return redirect(url_for('home'))
    
    username = session['username'] if 'username' in session else None
    loadmanager = User.get_loadmanager(username=username, api_key=api_key)
    
    manager = digitalocean.Manager(token=session["access_token"])
    my_droplets = manager.get_all_droplets()
    region = 'nyc3'
    droplet_name = 'spinupslave'
    size = '512mb'
    ipaddr = "http://"

    for droplet in my_droplets:
        if droplet.name == loadmanager:
            size = droplet.size_slug
            ipaddr += droplet.ip_address

    images = manager.get_all_images()
    image_id = None
    for image in images:
        if image.name == "SPINUP":
            image_id = image.id

    new_droplet = digitalocean.Droplet(
            token=session['access_token'],
            name=droplet_name,
            region=region,
            size_slug=size,
            image=image_id,
            )

    new_droplet.create()
    dropid = new_droplet.id
    url = "https://api.digitalocean.com/v2/droplets/" + str(dropid) 

    headers = {'content-type': 'application/json',
                'Authorization': 'Bearer ' + session['access_token'],
            }

    time.sleep(10)
   
    if not 'skip' in request.args:
        time.sleep(20) 
    response = requests.get(url, headers=headers)
    s = json.loads(response.text)


    new_ipaddr = "http://" + s['droplet']['networks']['v4'][0]['ip_address'] + ":9003"
    ipaddr += ":9002/service"
    t = "add-server"

    data = {
        'type':t,
        'url':new_ipaddr
    }

    requests.post(ipaddr, data=data)
    return redirect(url_for('home'))

@app.route('/stats/lastStat/<api_key>')
def lastStat(api_key):
    request = Data.get(api_key)

    resp = {}
    datum = next(request, None)
    if datum:
        # compare time of last request to datum
        datum_time = datum['timestamp']
        if 'last_request' not in session or \
            datetime.strptime(session['last_request'], "%d:%m:%y:%H:%M:%S") < datum_time:
            for k,v in datum.items():
                # skip built-in keys
                if k in ['datatype', 'timestamp', 'api_key', '_id']:
                    continue

                k = k.encode('ascii', 'ignore')
                resp[k] = v

    # update last_request with current time
    now = datetime.now()
    session['last_request'] = now.replace(second=(now.second - 2)%60).strftime("%d:%m:%y:%H:%M:%S")
    print datetime.strptime(session['last_request'], "%d:%m:%y:%H:%M:%S")

    return json.dumps(resp)

if __name__ == '__main__':
    app.run('0.0.0.0', 9001, debug=True)
