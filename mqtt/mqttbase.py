import time
import serial
import paho.mqtt.client as paho

broker = "10.72.7.151"
port = '/dev/ttyUSB0'  
bautRate = 9600

try:
    ser = serial.Serial(port, bautRate, timeout=None)
    arduino = 'ada'
    #startNyelem = 1000
except:
    arduino = 'gada'
    print('------------gada arduino------------')

def on_message(client, userdata, message):
    
    sumber = message.topic
    isi = str(message.payload.decode("utf-8"))
    
    if (sumber == "warna"):
        # ser.write(isi.encode())
        print(sumber, isi)



# MQTT
Broker = broker
client = paho.Client("Laptop")
client.connect(Broker)
client.loop_start()
print('subscribe oke')

while(True):
    client.subscribe("warna")
    client.on_message=on_message
    time.sleep(1)
    # client.publish("SPBU","a")
    # print("done")

    # for i in range(20):
    #     client.publish("Damkar", str(i))
    #     time.sleep(1)