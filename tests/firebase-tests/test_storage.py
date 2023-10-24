import pyrebase
import json

with open("./firebase-tests/cloud_server_credentials.json", "r") as credentials:
    firebase_config = json.load(credentials)

firebase = pyrebase.initialize_app(firebase_config)

storage = firebase.storage()

storage.child('route_execution').child('images/Screenshot_1').put('Screenshot_1.jpg')

storage.child('route_execution').child('images/Screenshot_1').download('downloaded_Screenshot_1.jpg')
