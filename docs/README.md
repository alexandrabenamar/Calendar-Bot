# Eliza-Bot
Eliza helps you check and modify your Google Calendar, Google Drive and do a research on Google or Youtube.
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

Start a virtual environment in your project path (for MacOs and Linux) : 

```
python3 -m venv env
source env/bin/activate
```

Run Flask web app : <br />
```
flask run
```

Go to http://127.0.0.1:5000 to run your app


## Author

Alexandra Benamar
