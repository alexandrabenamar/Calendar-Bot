##!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, make_response
import json, os, re
import dialogflow
import requests
import pusher

from Credentials import getCredentials
from EventManager import *
from CalendarManager import *
from drive import drive_credentials, search_file, open_file, share_file
from research import google_search, youtube_search, news_search

import uuid, string, random
import datetime
import dateutil.parser

app = Flask(__name__)

pusher_client = pusher.Pusher(
  app_id=APP_ID,
  key=KEY,
  secret=SECRET,
  cluster='eu',
  ssl=True
)

@app.route('/')
def index():
    return render_template('index.html')

def webHoookResult(req):

    result = req.get("result")
    action = result.get('action')

    ################## GOOGLE CALENDAR ACTIONS ##################

    if action == 'get_events':
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)
        calendar_service = createService()
        date = params.get('date')
        time=str(date)+"T00:00:01Z"

        response=getUpcomingEvents(calendar_service, time)
        reply = {
            "speech": response,
        }
        return jsonify(reply)

    elif action == "add_event":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        date = params.get('date')
        time = params.get('time')
        geo = params.get('geo-city')
        person = params.get('name')
        calendar_service = createService()
        summary = "Rendez-vous avec "+person

        t_start = time.split('/')[0]
        t_end = time.split('/')[1]

        d_start=str(date[0])+"T"+str(t_start)
        d_end=str(date[0])+"T"+str(t_end)

        event = {
            "summary": summary,
            "location": geo,
            'start':   {'dateTime': d_start, "timeZone": "Europe/Paris"},
            'end':     {'dateTime': d_end, "timeZone": "Europe/Paris"},
        }
        addEvent(calendar_service, event)

    ################## GOOGLE DRIVE ACTIONS ##################

    elif action == "open_drive":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        file = params.get('file-name')
        drive_service=drive_credentials()
        response=open_file(drive_service, file)
        reply = {
            "speech": response,
        }
        return jsonify(reply)

    elif action == "share-drive":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        file_name = params.get('file-name')
        email = params.get('user-email')
        option = str(params.get('option'))

        if option=="lecture":
            role="reader"
        elif re.search(r'criture', option):
            role="writer"
        elif re.search(r'propri', option):
            role="owner"
        else:
            response="Je n'ai pas compris les droits que vous souhaitez accorder."
            reply = {
                "speech": response,
            }
            return jsonify(reply)

        drive_service=drive_credentials()
        share_file(drive_service, file_name, email, role)

    ################## RESEARCH ACTIONS ##################

    elif action == "google-search":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        query = params.get('query')
        google_search(query)

    elif action == "youtube-search":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        query = params.get('query')
        youtube_search(query)

    elif action == "news-search":
        params = result.get("parameters")
        if len(params) == 0:
            return ([],None)

        response=news_search()
        reply = {
            "speech": response,
        }
        return jsonify(reply)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True,force=True)
    res = webHoookResult(req)
    if (res!=None):
        return res
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
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
