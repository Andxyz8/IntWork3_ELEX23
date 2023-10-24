import pyrebase
import json

with open("./firebase-tests/cloud_server_credentials.json", "r") as credentials:
    firebase_config = json.load(credentials)

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()

# Data to be inserted on realtime database
data_rnd_key = {'nome': "Testonildo", "Sobrenome": "Teste", "idade": "20"}
data_own_key = {'nome': "Testante", "Sobrenome": "Testeira", "idade": "40"}
data_update = {"idade": "41"}

# Push info with a random key to the data
_ = input("Wait.")
db.child('users').push(data_rnd_key)

# Push info with a own key to the data
_ = input("Wait..")
db.child('users').child("1").set(data_own_key)

# Updating info
_ = input("Wait...")
db.child('users').child("1").update(data_update)

# Retrieving info
_ = input("Wait....")
users = db.child('users').get()

for user in users.each():
    print(user.key())
    print(user.val())

_ = input("Wait....")
# Deleting info
db.child('users').child('-NgvV0w2lFLhqUMzL3XL').remove()

print('Finalizado!')
