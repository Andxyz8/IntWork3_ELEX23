from json import load as json_load
from requests import get as requests_get
from pyrebase.pyrebase import Storage, Firebase
from pyrebase import initialize_app as pyrebase_initialize_app
from utils.datetime_operator import get_str_datetime_agora
from database.rds_database import RDSDatabase

class DatabaseController:
    def __init__(self) -> None:
        self.__firebase: Firebase = None
        self.__cloud_database: RDSDatabase = None
        self.__cloud_storage: Storage = None
        self.__firebase_config = None

        if not self.__initialize_firebase():
            raise Exception("It was not possible to initialize firebase.")

    def __initialize_firebase(self) -> bool:
        with open("./database/credentials.json", "r", encoding = 'utf-8') as credentials:
            firebase_config = json_load(credentials)

        self.__firebase = pyrebase_initialize_app(firebase_config)

        self.__cloud_storage = self.__firebase.storage()

        self.__cloud_database = RDSDatabase()

        return True

    def get_next_id_collection(self, collection: str) -> int:
        url = (
                "https://mall-security-robot-e52f0-default-rtdb.firebaseio.com/"
                + f"{collection}.json?orderBy=%22id_{collection}%22&limitToLast=1"
            )

        response = requests_get(
            url = url,
            timeout = 5
        )

        print(f"URL REQUEST: {url}")

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

    def insert_route_recording(
        self,
        title: str,
        description: str,
        n_repeats: int,
        interval_between_repeats: str
    ) -> int:
        query_insert = f"""
            INSERT INTO route(
                title,
                description,
                status,
                number_repeats,
                interval_between_repeats,
                created_at
            ) VALUES(
                '{title}',
                '{description}',
                'Active',
                {n_repeats},
                TIMESTAMP '{interval_between_repeats}',
                TIMESTAMP '{get_str_datetime_agora()}'
            ) RETURNING id_route;
        """
        id_route_execution = self.__cloud_database.execute_insert(
            query_insert,
            return_id = True
        )
        return id_route_execution

    def insert_route_steps(self, id_route: int, route_steps: dict[str, str]) -> None:
        for step in route_steps:
            query_insert = f"""
                INSERT INTO route_steps(
                    id_route,
                    step_sequence,
                    start_aruco_marker,
                    next_aruco_marker,
                    number_rotations_left_encoder,
                    number_rotations_right_encoder,
                    left_pwm_intensity,
                    right_pwm_intensity,
                    compass_module_degrees
                ) VALUES (
                    {id_route},
                    '{step['step_sequence']}',
                    {step['start_aruco_marker']},
                    {step['next_aruco_marker']},
                    {step['number_rotations_left_encoder']},
                    {step['number_rotations_right_encoder']},
                    {step['left_pwm_intensity']},
                    {step['right_pwm_intensity']},
                    {step['compass_module_degrees']}
                );
            """
            self.__cloud_database.execute_insert(query_insert)

    def insert_route_execution(self, id_route: int, id_robot: int) -> int:
        """Insert a new route execution register in the cloud database.

        Returns:
            bool: True if successful, False otherwise.
        """
        query_insert = f"""
            INSERT INTO route_execution(
                id_route,
                id_robot,
                moment_start
            ) VALUES(
                {id_route},
                {id_robot},
                TIMESTAMP '{get_str_datetime_agora()}'
            ) RETURNING id_route_execution;
        """
        id_route_execution = self.__cloud_database.execute_insert(
            query_insert,
            return_id = True
        )
        return id_route_execution

    def update_route_ending(self, unique_id: int) -> bool:
        """Update the ending of a route.
        
        Args:
            unique_id (int): id_route_execution of the route.
        """
        query_update = f"""
            UPDATE route_execution
            SET
                moment_end = TIMESTAMP '{get_str_datetime_agora()}'
            WHERE id_route_execution = {unique_id};
        """
        self.__cloud_database.execute_update(query_update)

    def insert_alarm_triggering(self) -> bool:
        """Inserts a alarm triggering at the cloud database."""
        raise NotImplementedError

    def insert_camera_triggering(
        self,
        id_route_execution: int,
        reason: str,
        image_url: str
    ) -> bool:
        """Inserts a camera triggering at the cloud database."""
        query_insert = f"""
            INSERT INTO camera_triggering (
                id_route_execution,
                reason,
                image_url,
                moment
            ) VALUES (
                '{id_route_execution}',
                '{reason}',
                '{image_url}',
                TIMESTAMP '{get_str_datetime_agora()}'
            );
        """
        self.__cloud_database.execute_insert(query_insert)

        return True
