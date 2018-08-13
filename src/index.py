# /index.py

from flask import Flask, request, jsonify, render_template, make_response
import os
import dialogflow
import requests
import json
import pusher
from Credentials import getCredentials
from EventManager import *
from CalendarManager import *
import uuid
import string
import random
from datetime import datetime


app = Flask(__name__)

pusher_client = pusher.Pusher(
  app_id='577057',
  key='c6e47f1a8cdf65a93c8e',
  secret='e4a72ba63936c2436523',
  cluster='eu',
  ssl=True
)

@app.route('/')
def index():
    return render_template('index.html')


def webHoookResult(req):

    result = req.get("result")
    action = result.get('action')

    if action == 'get_events':
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)
        date = params.get('date')
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        CREDENTIAL_PATH = './credentials/client_secret.json'
        credentials = getCredentials(CREDENTIAL_PATH) #insert your client_secret.json file path
        service = build('calendar', 'v3', http=credentials.authorize(Http()))
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        response=getUpcomingEvents(service, now)
        reply = {
            "fulfillmentText": response,
        }
        return jsonify(reply)

    elif action == "add_event":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)
        date = params.get('date')
        geo = params.get('geo-city')
        personne = params.get('last-name')
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        CREDENTIAL_PATH = './credentials/client_secret.json'
        credentials = getCredentials(CREDENTIAL_PATH) #insert your client_secret.json file path
        service = build('calendar', 'v3', http=credentials.authorize(Http()))
        summary = "Rendez-vous avec "+personne

        GMT_OFF = '+02:00'
        event = {
            "summary": summary,
            "location": geo,
            'start':   {'dateTime': '2018-08-14T09:00:00%s' % GMT_OFF},
            'end':     {'dateTime': '2018-08-14T17:00:00%s' % GMT_OFF},
        }
        response=addEvent(service, event)
        reply = {
            "fulfillmentText": response,
        }
        return jsonify(reply)

    else:
        return ([],None)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True,force=True)
    res = webHoookResult(req)
    r = make_response(res)
    r.headers['Content-type'] = 'application/json'
    return r


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    socketId = request.form['socketId']
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    pusher_client.trigger('Eliza', 'new_message',
                        {'human_message': message, 'bot_message': fulfillment_text})

    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run(debug=True)
