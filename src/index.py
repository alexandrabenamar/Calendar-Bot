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

# your flask web app
app = Flask(__name__)

# Enter your pusher app informations
pusher_client = pusher.Pusher(
  app_id=APP_ID,
  key=KEY,
  secret=SECRET,
  cluster=CLUSTER,
  ssl=True
)

@app.route('/')
def index():
    """
        Main function of the web app
    """
    return render_template('index.html')

def webHoookResult(req):
    """
        Execute the action for the user.
    """

    result = req.get("result")
    action = result.get('action')

    if action == 'get_events':
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)
        service = createService()
        date = params.get('date')       ##dialogflow format : @sys.date
        time=str(date)+"T00:00:01Z"

        response=getUpcomingEvents(service, time)
        reply = {
            "speech": response,
        }
        return jsonify(reply)

    elif action == "add_event":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        date = params.get('date')          #dialogflow format : @sys.date
        time = params.get('time')          #dialogflow format : @sys.time-period
        geo = params.get('geo-city')       #dialogflow format : @sys.geo-city
        person = params.get('last-name')   #dialogflow format : @sys.any
        service = createService()
        summary = "Meeting with "+person

        t_start = time.split('/')[0]
        t_end = time.split('/')[1]

        # converting into ISO-8601gi format
        d_start=str(date[0])+"T"+str(t_start)
        d_end=str(date[0])+"T"+str(t_end)

        # creating the event
        event = {
            "summary": summary,
            "location": geo,
            'start':   {'dateTime': d_start, "timeZone": "Europe/Paris"},
            'end':     {'dateTime': d_end, "timeZone": "Europe/Paris"},
        }
        addEvent(service, event)


@app.route('/webhook', methods=['POST'])
def webhook():
    """
        Function triggered by dialogflow API.
        Create the response for the user.
    """
    req = request.get_json(silent=True,force=True)
    res = webHoookResult(req)           # complete the action
    if (res!=None):                     # if there is a specific response for the action
        return res                      # then return the response
    res = json.dumps(res, indent=4)
    r = make_response(res)              # else search for the default response
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
