import webbrowser
from flask import Flask, render_template, request, send_file
from threading import Thread
import time
import requests
import os
import signal

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', current_track=current_track)

@app.route('/tracks')
def tracks():
    trackname = request.args.get('name')
    # return the track in ../../generated/track_name.mid
    return send_file(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'generated',trackname+'.mid'))

@app.route('/shutdown')
def shutdown():
    # When you need to stop the server
    os.kill(os.getpid(), signal.SIGKILL)
    return 'Server shutting down...'

def start_flask_server():
    app.run(host='127.0.0.1', port=5000)
    os.kill(os.getpid(), signal.SIGKILL)

def play(track):
    global current_track 
    current_track = track.split('/')[-1].split('.')[0]
    # Start the Flask server in a separate thread
    server_thread = Thread(target=start_flask_server)
    server_thread.start()

    # Wait a short moment to ensure the server starts
    time.sleep(1)

    # Open the web browser
    url = 'http://127.0.0.1:5000'
    webbrowser.open(url)

    # sleep for 10 seconds
    time.sleep(1)

    # Shutdown the server
    # requests.get(url + '/shutdown')