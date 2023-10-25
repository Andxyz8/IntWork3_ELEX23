from json import load as json_load
from requests import get as requests_get
from pyrebase.pyrebase import Database, Storage, Firebase
from pyrebase import initialize_app as pyrebase_initialize_app

class DatabaseController:
    def __init__(self) -> None:
        self.__firebase: Firebase = None
        self.__cloud_database: Database = None
        self.__cloud_storage: Storage = None
        self.__firebase_config = None

        if not self.__initialize_firebase():
            raise Exception("Não foi possível inicializar o Firebase")

        print("DATABASES INICIALIZADO COM SUCESSO")

    def __initialize_firebase(self) -> bool:
        try:
            with open("./database/credentials.json", "r") as credentials:
                firebase_config = json_load(credentials)
            
            print(firebase_config)

            self.__firebase = pyrebase_initialize_app(firebase_config)

            self.__cloud_storage = self.__firebase.storage()

            self.__cloud_database = self.__firebase.database()
        except Exception:
            return False
        return True

    def get_next_id_collection(self, collection: str) -> int:
        url = (
                "https://mall-security-robot-e52f0-default-rtdb.firebaseio.com/"
                + f"{collection}.json?orderBy=%22id_{collection}%22&limitToLast=1"
            )
        print(f"URL BUSCA id: {url}")
        response = requests_get(
            url = url
        )

        records = response.json()

        for item in records:
            record = records[item]
            break

        if response.status_code == 200:
            last_key_inserted = record[f'id_{collection}']
            next_key = int(last_key_inserted) + 1
        else:
            next_key = 1
        
        return next_key

    def update_data_into_collection(
        self,
        collection: str,
        unique_id: int,
        info_insert: dict
    ) -> bool:
        print(f"UPDATE REALTIME DATABASE {collection} [{unique_id}]: {info_insert}")
        self.__cloud_database.child(collection).child(unique_id).update(info_insert)
        return True

    def insert_data_into_collection(self, collection: str, info_insert: dict) -> bool:
        print(f"INSERT REALTIME DATABASE {collection}: {info_insert}")

        self.__cloud_database.child(collection).push(info_insert)

        return True
