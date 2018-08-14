##!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, make_response
import os
import dialogflow
import requests
import json
import pusher
from Credentials import getCredentials
from EventManager import *
from CalendarManager import *
import uuid, string, random
import dateutil.parser


app = Flask(__name__)

pusher_client = pusher.Pusher(
  app_id=APP_ID,
  key=KEY,
  secret=SECRET,
  cluster=CLUSTER,
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
        service = createService()
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        response=getUpcomingEvents(service, now)
        reply = {
            "speech": response,
        }
        return jsonify(reply)

    elif action == "add_event":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        time = params.get('time-period')
        geo = params.get('geo-city')
        personne = params.get('last-name')
        service = createService()
        summary = "Rendez-vous avec "+personne

        d_start = time.split('/')[0]
        d_start = time.split('/')[1]

        event = {
            "summary": summary,
            "location": geo,
            'start':   {'dateTime': d_start, "timeZone": "Europe/Paris"},
            'end':     {'dateTime': d_end, "timeZone": "Europe/Paris"},
        }
        addEvent(service, event)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True,force=True)
    res = webHoookResult(req)
    if (res!=None):
        return res
    res = json.dumps(res, indent=4)
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


if __name__ == "__main__":
    app.run(debug=True)
