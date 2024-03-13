from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
import time
import datetime
main = Blueprint('main', __name__)

values = {}
url_timestamp = {}
url_viewtime = {}
wwwtime = {}
prev_url = ""
curr_url = ""

def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '') .replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url




@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/processes')
@login_required
def processes():
    return render_template('processes.html')

@main.route('/hardware')
@login_required
def hardware():
    return render_template('hardware.html')



@main.route('/send_url',  methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    print("currently viewing: " + url_strip(url))
    parent_url = url_strip(url)
    global url_timestamp
    global url_viewtime
    global wwwtime
    global prev_url
    global values
    
    
    print("initial db prev tab: ", prev_url)
    print("initial db timestamp: ", url_timestamp)
    print("initial db viewtime: ", url_viewtime)

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    x = int(time.time())
    url_timestamp[parent_url] = x
    wwwtime[parent_url] = datetime.datetime.fromtimestamp(x).strftime('%c')
    prev_url = parent_url
    print("final timestamps: ", url_timestamp)
    print("final viewtimes: ", url_viewtime)
    print('test', (time.asctime( time.localtime(x) )))
    

    return jsonify({'message': 'success!'}), 200

@main.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

@main.route('/websitetracker')
@login_required
def websiteTracker():
    return render_template('websiteTracker.html')
