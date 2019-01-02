# Eliza
Eliza helps you handle your Google Calendar and Google Drive and also research queries on Google or Youtube.

Eliza was created to handle your Google account by adding or researching for events in your Google Calendar and also research, open and share a Google Drive file and research queries on Google or YouTube. This assistant also allows you to check on the last news in innovation and technologies. Moreover, Eliza can also handle small talk dialog and discuss with its user.

This project was created using Dialogflow, Flask and Pusher.

## Implementation

Language version : Python 3.6. <br />
Operating System : MacOS High Sierra.

## Getting Started

### Libraries

Install the set of dependencies : <br />
```
pip install -r requirements.txt
```

### Google Calendar API

The code to handle Google Calendar API is available here : <br />
https://github.com/alexandrabenamar/GoogleCalendarManager

### Google Drive API

The code to handle Google Drive API is available here : <br />
https://github.com/alexandrabenamar/GoogleDriveManager

### Get your Pusher API Key

Create a free account on Pusher (https://pusher.com/channels). Then create a new app and write dows your app_id,
key, secret and cluster. You'll need Pusher Channels to add real-time funtionnalities to your bot.

### News API

News API is a simple and easy-to-use API that returns JSON metadata for headlines and articles live all over the web right now. Get your API-key to add the functionnality to your bot (https://newsapi.org/docs/get-started).


## Execution

### Setup a virtual environment

Use a secure tunnel to localhost webhook development tool and debugging tool. I personnaly use ngrok : <br />
```
ngrok http localhost:5000
```

Create a virtual environment in your project path using : <br />
```
python3 -m venv env
```
or : <br />
```
python -m venv env
```

##### MacOs or Linux

Activate the virtual environment : <br />
```
source env/bin/activate
```

#### Windows

Activate the virtual environment : <br />
```
env/Scripts/activate
```

### Run your app

Run Flask web app : <br />
```
flask run
```

Go to http://127.0.0.1:5000 to run your app


## Author

Alexandra Benamar
