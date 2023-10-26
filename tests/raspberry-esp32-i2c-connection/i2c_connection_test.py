from time import sleep
from smbus2 import SMBus

slave_address = 0x18
i2c_bus = SMBus(1)
def read_data_from_esp32():
    dados_recebidos_esp = i2c_bus.read_i2c_block_data(
    slave_address,
            0,
            12,
            True
    )

    msg_received = ''
    for i in range(len(dados_recebidos_esp)):
        msg_received += chr(dados_recebidos_esp[i])
    return msg_received

def send_data_to_esp32(message_to_send: str):
    # message_to_send = "Hi, from Raspberry PI 3"
    bytes_message = message_to_send.encode('utf-8')

    i2c_bus.write_i2c_block_data(
        slave_address,
        0,
        bytes_message,
        False
    )

def read_onboard_led_status_from_esp():
    command_read = 'xcb'
    send_data_to_esp32(command_read)

    mensagem_recebida = read_data_from_esp32()
    print(f"VALOR: {mensagem_recebida}")

while 1:
    option = input("1 - Read onboard status from ESP.\n2 - Send to ESP.\nOption: ")
    if option == '1':
        read_onboard_led_status_from_esp()
    elif option == '2':
        message = input("SEND: ")
        send_data_to_esp32(message)
    sleep(0.01)
