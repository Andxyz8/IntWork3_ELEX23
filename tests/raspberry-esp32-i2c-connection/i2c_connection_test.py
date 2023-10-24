#Programa: Python Raspberry Pi Comunicacao I2C
#Autor: Arduino e Cia
#!/usr/bin/python
from time import sleep
from smbus2 import SMBus

slave_address = 0x18
bus = SMBus(1)

def read_data_from_esp():
    msg_recebida = ""
    dados_recebidos_Arduino = bus.read_i2c_block_data(
        slave_address,
        0,
        12,
        True
    )
    for i in range(len(dados_recebidos_Arduino)):
        msg_recebida += chr(dados_recebidos_Arduino[i])
    print(msg_recebida)
    dados_recebidos_Arduino = ""


def send_data_to_esp32():
    str_message = "Hi, from Raspberry PI 3"
    bytes_message = str_message.encode('utf-8')
    bus.write_i2c_block_data(
        slave_address,
        0,
        bytes_message,
        True
    )

while 1:
    read_data_from_esp()
    send_data_to_esp32()
    sleep(0.25)
