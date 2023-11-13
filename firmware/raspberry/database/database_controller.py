from json import load as json_load
from uuid import uuid4 as generate_uuid
from pandas import DataFrame
from pyrebase.pyrebase import Storage, Firebase
from pyrebase import initialize_app as pyrebase_initialize_app
from utils.datetime_operator import get_str_datetime_agora
from database.rds_database import RDSDatabase

class DatabaseController:
    __firebase: Firebase
    __cloud_database: RDSDatabase
    __cloud_storage: Storage

    def __init__(self) -> None:
        self.__initialize_firebase()

    def __initialize_firebase(self) -> bool:
        # Open credentials archive stored locally in the raspberry
        with open(
            file = "./database/credentials.json",
            mode = "r",
            encoding = 'utf-8'
        ) as credentials:
            firebase_config = json_load(credentials)

        # Initialize the Firebase instance to get access to the Storage
        self.__firebase = pyrebase_initialize_app(firebase_config)

        # Get the instance of the Storage used
        self.__cloud_storage = self.__firebase.storage()

        # Instantiate the rds cloud database operator
        self.__cloud_database = RDSDatabase()

        return True

    def __upload_image_to_cloud_storage(self, image_unique_id: str) -> str:
        """Upload an image to the cloud storage and return its URL.

        Args:
            image_unique_id (str): unique id of the image stored locally.

        Returns:
            str: url of the image in the cloud storage.
        """
        # endpoint_firebase = f"route_execution/{image_unique_id}"
        path_image_locally =  f"./handlers/.imgs/{image_unique_id}.jpeg"

        response = self.__cloud_storage.child(
            'route_execution'
        ).child(image_unique_id).put(path_image_locally)

        print(f"RESPONSE: {response}")

        path_image_storage = f"route_execution/{image_unique_id}"
        firebase_url_image = self.__cloud_storage.child(
            path_image_storage
        ).get_url(response['downloadTokens'])

        return firebase_url_image

    def __insert_camera_triggering(
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

    def __insert_alarm_triggering(self, id_route_execution: int, reason: str) -> bool:
        """Inserts a alarm triggering at the cloud database."""
        query_insert = f"""
            INSERT INTO alarm_triggering (
                id_route_execution,
                reason,
                moment
            ) VALUES (
                {id_route_execution},
                '{reason}',
                TIMESTAMP '{get_str_datetime_agora()}'
            );
        """
        self.__cloud_database.execute_insert(query_insert)

        return True

    def insert_route_recording_start(self) -> int:
        query_insert = f"""
            INSERT INTO route(
                status,
                created_at
            ) VALUES(
                'Active',
                TIMESTAMP '{get_str_datetime_agora()}'
            ) RETURNING id_route;
        """
        id_route_execution = self.__cloud_database.execute_insert(
            query_insert,
            return_id = True
        )
        return id_route_execution

    def update_route_recording_end(
        self,
        id_route: int,
        title: str,
        description: str,
        n_repeats: int,
        interval_between_repeats: float
    ) -> None:
        query_update = f"""
            UPDATE route SET
                title = '{title}',
                description = '{description}',
                n_repeats = {n_repeats},
                interval_between_repeats = {interval_between_repeats}
            WHERE id_route = {id_route};
        """
        self.__cloud_database.execute_update(query_update)

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

    def insert_route_execution_movement_detection(
        self,
        id_route_execution: int,
        image_unique_id: str,
        step_sequence: str
    ) -> bool:
        firebase_image_url = self.__upload_image_to_cloud_storage(image_unique_id)
        triggering_reason = "Movement Detection"
        self.__insert_camera_triggering(
            id_route_execution = id_route_execution,
            reason = triggering_reason,
            image_url = firebase_image_url
        )
        self.__insert_alarm_triggering(
            id_route_execution = id_route_execution,
            reason = triggering_reason
        )
        return True

    def update_route_execution_ending(self, unique_id: int) -> bool:
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

    def insert_notification(
        self,
        id_route_execution: int,
        message: str,
        value: str
    ) -> bool:
        """Insert a new row into the notification table.
        
        - Useful to communicate current exection status to the mobile app.
        """
        query_insert = f"""
            INSERT INTO notification(
                id_route_execution,
                message,
                value,
                moment
            ) VALUES (
                {id_route_execution},
                '{message}',
                '{value}',
                TIMESTAMP '{get_str_datetime_agora()}'
            );
        """
        self.__cloud_database.execute_insert(query_insert)

    def get_route_steps(self, id_route: int) -> DataFrame:
        query_select = f"""
            SELECT 
                step_sequence,
                start_aruco_marker,
                next_aruco_marker,
                number_rotations_left_encoder,
                number_rotations_right_encoder,
                left_pwm_intensity,
                right_pwm_intensity,
                compass_module_degrees
            FROM route_steps
            WHERE id_route = {id_route};
        """
        df_route_steps = self.__cloud_database.execute_select(query_select)
        return df_route_steps
