from struct import unpack, pack
from smbus2 import SMBus
from numpy import nan

class ESPCommunicationHandler:

    def __init__(self) -> None:
        self.__i2c_slave_adress = 0x18
        self.__i2c_bus = SMBus(1)
        self.__dict_commands: dict[str, str] = {
            'READ_COMPASS': 'crc', # not implemented
            'COMMUNICATION_TEST': 'mct', # implemented
            'TURN_OFF_BUZZER': 'tib', # not implemented
            'TURN_ON_BUZZER': 'tab', # not implemented
            'READ_BUZZER': 'rbs', # not implemented
            'READ_RIGHT_ENCODER': 'rre', # not implemented
            'READ_LEFT_ENCODER': 'rle', # not implemented
            'MOVE_FORWARD': 'cmf', # implemented on esp
            'MOVE_FORWARD_FINE': 'cff',
            'MOVE_BACKWARD': 'cmb', # implemented on esp
            'ROTATE_LEFT': 'crl', # implemented on esp
            'ROTATE_RIGHT': 'crr', # implemented on esp
            'PLACE_CAMERA_SERVO_CENTER': 'csm', # implemented on esp
            'TURN_CAMERA_SERVO_RIGHT': 'csf', # implemented on esp
            'TURN_CAMERA_SERVO_LEFT': 'csz' # implemented on esp
        }

    def __read_data_from_esp32(self, size_to_read: int) -> list[int]:
        # Read size_to_read bytes from i2c interface with esp32
        data_received_esp = self.__i2c_bus.read_i2c_block_data(
            self.__i2c_slave_adress,
            0,
            size_to_read,
            False
        )
        print(f"DATA RECEIVED FROM ESP32: {data_received_esp}")

        return data_received_esp

    def __send_command_to_esp32(self, data_to_send: str) -> None:
        bytes_data = self.__dict_commands[data_to_send].encode('utf-8')

        self.__i2c_bus.write_i2c_block_data(
            self.__i2c_slave_adress,
            0,
            bytes_data,
            False
        )

    def __send_float_to_esp32(self, float_to_send: float) -> None:
        bytes_data = pack('f', float_to_send)

        self.__i2c_bus.write_i2c_block_data(
            self.__i2c_slave_adress,
            0,
            bytes_data,
            False
        )

    def __read_str_from_data_from_esp32(self) -> str:
        data_received_esp = self.__read_data_from_esp32(4)

        # Initialize empty the complete message from esp32
        msg_received = ''

        # For loop to construct a char response for every byte received
        for byte_received in data_received_esp:
            msg_received += chr(byte_received)

        print(f"STRING RECEIVED: {msg_received}")

        return msg_received

    def __read_float_from_data_from_esp32(self) -> float:
        data_received_esp = self.__read_data_from_esp32(4)

        bytes_float = bytes(data_received_esp)

        float_return = unpack('f', bytes_float)
        print(f"isinstance(float_return, tuple): {isinstance(float_return, tuple)}")
        if isinstance(float_return, tuple):
            float_return = float_return[0]

        print(f"not isinstance(float_return, float): {not isinstance(float_return, float)}")
        if not isinstance(float_return, float):
            return 0.0

        print(f"float_return == nan: {float_return == nan}")
        if float_return == nan:
            return 0.0

        print(f"FLOAT RECEIVED: {float_return}")

        return float_return

    def __test_i2c_communication_with_esp32(self) -> bool:
        self.__send_command_to_esp32('COMMUNICATION_TEST')
        esp_status = self.__read_str_from_data_from_esp32()

        print(f"ESP STATUS: {esp_status}")

        if 'OK' in esp_status:
            return True
        return False

    def __read_buzzer_status(self) -> int:
        self.__send_command_to_esp32('READ_BUZZER')
        data = self.__read_float_from_data_from_esp32()
        retry_number = 5
        retries = 0
        while data == nan:
            if retries == retry_number:
                return 0.0
            print(f"COMPASS MODULE DATA CORRUPTED: {data}")
            self.__send_command_to_esp32('READ_COMPASS')
            data = self.__read_float_from_data_from_esp32()

            retries += 1

        print(f"COMPASS MODULE DATA: {data}")

        try:
            return round(float(data), 2)
        except ValueError:
            return 0.0

    def __read_left_encoder_info(self) -> float:
        self.__send_command_to_esp32('READ_LEFT_ENCODER')
        data = self.__read_float_from_data_from_esp32()
        retry_number = 5
        retries = 0
        while data == nan:
            if retries == retry_number:
                return 0.0
            print(f"LEFT ENCODER DATA CORRUPTED: {data}")
            self.__send_command_to_esp32('READ_LEFT_ENCODER')
            data = self.__read_float_from_data_from_esp32()

            retries += 1

        print(f"LEFT ENCODER DATA: {data}")

        try:
            return round(float(data), 2)
        except ValueError:
            return 0.0

    def __read_right_encoder_info(self) -> float:
        self.__send_command_to_esp32('READ_RIGHT_ENCODER')
        data = self.__read_float_from_data_from_esp32()
        retry_number = 5
        retries = 0
        while data == nan:
            if retries == retry_number:
                return 0.0
            print(f"RIGHT ENCODER DATA CORRUPTED: {data}")
            self.__send_command_to_esp32('READ_RIGHT_ENCODER')
            data = self.__read_float_from_data_from_esp32()

            retries += 1

        print(f"RIGHT ENCODER DATA: {data}")

        try:
            return round(float(data), 2)
        except ValueError:
            return 0.0

    def __read_compass_info(self) -> float:
        self.__send_command_to_esp32('READ_COMPASS')
        data = self.__read_float_from_data_from_esp32()

        retry_number = 5
        retries = 0
        while data == nan:
            if retries == retry_number:
                return 0.0
            print(f"COMPASS MODULE DATA CORRUPTED: {data}")
            self.__send_command_to_esp32('READ_COMPASS')
            data = self.__read_float_from_data_from_esp32()

            retries += 1

        print(f"COMPASS MODULE DATA: {data}")

        try:
            return round(float(data), 2)
        except ValueError:
            return 0.0

    def test_esp32_i2c_communication(self) -> bool:
        if not self.__test_i2c_communication_with_esp32():
            retries = 0
            while not self.__test_i2c_communication_with_esp32():
                if retries >= 5:
                    break

                print("ESP32 I2C Communication with Raspberry Not Established.")
                print("Retrying Connection Test 3x...")

                for i in [3, 2, 1]:
                    print(f"{i}...")
                retries += 1

            if retries >= 5:
                return False
        return True

    def get_step_execution_info(self) -> dict[str, str]:
        right_encoder = self.__read_right_encoder_info()

        left_encoder = self.__read_left_encoder_info()

        buzzer_status = self.__read_buzzer_status()

        compass = self.__read_compass_info()

        return {
            "right_encoder": right_encoder,
            "left_encoder": left_encoder,
            "compass": compass,
            "buzzer_status": buzzer_status
        }

    def get_step_recording_info(self) -> dict[str, str]:
        right_encoder = self.__read_right_encoder_info()

        left_encoder = self.__read_left_encoder_info()

        compass = self.__read_compass_info()

        return {
            "right_encoder": right_encoder,
            "left_encoder": left_encoder,
            "compass": compass
        }

    def move_forward(self):
        self.__send_command_to_esp32('MOVE_FORWARD')
        data = self.__read_str_from_data_from_esp32()

        print(f"PWM MOTOR STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def move_forward_fine(
        self,
        pwm_intensity_left: float,
        pwm_intensity_right: float,
        time_in_seconds: int
    ) -> bool:
        self.__send_command_to_esp32('MOVE_FORWARD_FINE')

        self.__send_float_to_esp32(pwm_intensity_left)
        self.__send_float_to_esp32(pwm_intensity_right)
        self.__send_float_to_esp32(time_in_seconds)

        data = self.__read_str_from_data_from_esp32()

        print(f"PWM MOTOR STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def move_backward(self) -> bool:
        self.__send_command_to_esp32('MOVE_BACKWARD')
        data = self.__read_str_from_data_from_esp32()

        print(f"PWM MOTOR STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def rotate_left(self) -> bool:
        self.__send_command_to_esp32('ROTATE_LEFT')
        data = self.__read_str_from_data_from_esp32()

        print(f"PWM MOTOR STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def rotate_right(self) -> bool:
        self.__send_command_to_esp32('ROTATE_RIGHT')
        data = self.__read_str_from_data_from_esp32()

        print(f"PWM MOTOR STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def center_camera_servo(self) -> bool:
        self.__send_command_to_esp32('PLACE_CAMERA_SERVO_CENTER')
        data = self.__read_str_from_data_from_esp32()

        print(f"SERVO STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def rotate_camera_servo_right(self) -> bool:
        self.__send_command_to_esp32('TURN_CAMERA_SERVO_RIGHT')
        data = self.__read_str_from_data_from_esp32()

        print(f"SERVO STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def rotate_camera_servo_left(self) -> bool:
        self.__send_command_to_esp32('TURN_CAMERA_SERVO_LEFT')
        data = self.__read_str_from_data_from_esp32()

        print(f"SERVO STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def turn_off_buzzer(self) -> bool:
        self.__send_command_to_esp32('TURN_OFF_BUZZER')
        data = self.__read_str_from_data_from_esp32()

        print(f"BUZZER STATUS: {data}")

        if 'OK' in data:
            return True
        return False

    def turn_on_buzzer(self) -> bool:
        self.__send_command_to_esp32('TURN_ON_BUZZER')
        data = self.__read_str_from_data_from_esp32()

        print(f"BUZZER STATUS: {data}")

        if 'OK' in data:
            return True
        return False
