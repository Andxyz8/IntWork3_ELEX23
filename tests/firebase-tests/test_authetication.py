import pyrebase
import json

# Carrega as credencias do arquivo de configuração em json
with open("./firebase-tests/cloud_server_credentials.json", "r") as credentials:
    firebase_config = json.load(credentials)

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

email = input("Email: ")
senha = input("Senha: ")

user = auth.create_user_with_email_and_password(email, senha)

print('Finalizado!')

