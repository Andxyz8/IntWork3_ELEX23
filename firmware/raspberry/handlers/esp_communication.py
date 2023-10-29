from time import sleep as time_sleep
from smbus2 import SMBus
from struct import unpack
from numpy import nan

class ESPCommunicationHandler:

    def __init__(self) -> None:
        self.__i2c_slave_adress = 0x18
        self.__i2c_bus = SMBus(1)
        self.__dict_commands: dict[str, str] = {
            'READ_COMPASS': 'crc',
            'COMMUNICATION_TEST': 'mct'
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

    def __send_data_to_esp32(self, data_to_send: str) -> None:
        bytes_data = self.__dict_commands[data_to_send].encode('utf-8')

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

    def get_compass_module_data(self) -> float:
        self.__send_data_to_esp32('READ_COMPASS')
        data = self.__read_float_from_data_from_esp32()

        retry_number = 5
        retries = 0
        while data == nan:
            if retries == retry_number:
                return 0.0
            print(f"COMPASS MODULE DATA CORRUPTED: {data}")
            self.__send_data_to_esp32('READ_COMPASS')
            data = self.__read_float_from_data_from_esp32()

            retries += 1

        print(f"COMPASS MODULE DATA: {data}")

        try:
            return round(float(data), 2)
        except ValueError:
            return 0.0

    def __test_i2c_communication_with_esp32(self) -> bool:
        self.__send_data_to_esp32('COMMUNICATION_TEST')
        esp_status = self.__read_str_from_data_from_esp32()

        print(f"ESP STATUS: {esp_status}")

        if 'OK' in esp_status:
            return True
        return False

    def test_esp32_i2c_communication(self) -> bool:
        if not self.__test_i2c_communication_with_esp32():
            while not self.__test_i2c_communication_with_esp32():
                print("ESP32 I2C Communication with Raspberry Not Established.")
                print("Retrying Connection Test 3x...")
                for i in [3, 2, 1]:
                    print(f"{i}...")
        return True
