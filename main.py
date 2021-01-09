from flask import Flask, render_template
from flask_socketio import SocketIO
import json
from flask_cors import CORS
from flask import jsonify
import urllib
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

languageMapping = {"English": "en", "Spanish": "es"}

@app.route('/')
def sessions():
    return render_template('session.html')

@app.route('/getmessage/<jsdata>')
def translate(jsdata):
    j = json.loads(jsdata)
    if j["language_from"] != j["language"]:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + j["language_from"] + "&tl=" + j["language"] + "&dt=t&q=" + urllib.parse.quote(j["message"])
        result = requests.get(url).json()
        if result is not None:
            j["message"] = result[0][0][0]
        else:
            j["message"] += " (Untranslated due to API error)"
    return j

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('message event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    socketio.emit('message response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=False)