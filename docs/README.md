# Eliza-Bot
Eliza helps you handle your Google Calendar and Google Drive and also research queries on Google or Youtube.
This project was created using Dialogflow, Flask and Pusher.

## Implementation

Language version : Python 3.6. <br />
Operating System : MacOS High Sierra.

## Getting Started

### Google Calendar API

The code to handle Google Calendar API is available here : <br />
https://github.com/alexandrabenamar/GoogleCalendarManager

### Google Drive API

The code to handle Google Drive API is available here : <br />
https://github.com/alexandrabenamar/GoogleDriveManager

### Libraries

Install the set of dependencies : <br />
```
pip install -r requirements.txt
```
## Execution

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

### MacOs or Linux

Activate the virtual environment : <br />
```
source env/bin/activate
```

### Windows

Activate the virtual environment : <br />
```
env/Scripts/activate
```

Run Flask web app : <br />
```
flask run
```

Go to http://127.0.0.1:5000 to run your app


## Author

Alexandra Benamar
