from handlers.esp_communication import ESPCommunicationHandler


class InitialStateMediator:
    def __init__(self, ctrl_esp: ESPCommunicationHandler) -> None:
        self.ctrl_esp: ESPCommunicationHandler = ctrl_esp

    def test_esp32_i2c_communication(self) -> bool:
        return self.ctrl_esp.test_esp32_i2c_communication()
