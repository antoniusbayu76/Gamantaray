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
    
    if sumber == "kamera samping" and isi == "a" :
        if arduino == 'ada' :
            ser.write(isi.encode())
        print(sumber, isi)
    elif sumber == "kamera depan" :
        if arduino == 'ada':
            ser.write(isi.encode())
        print(sumber, isi)

Broker = broker
client1 = paho.Client("depan")
client2 = paho.Client("samping")

client1.connect(Broker)
client2.connect(Broker)

client1.loop_start()
client2.loop_start()
print('subscribe oke')

while(True):
    client1.subscribe("kamera depan")
    client2.subscribe("kamera samping")

    client1.on_message=on_message
    client2.on_message=on_message
    # client.publish("SPBU","a")
    # print("done")

    # for i in range(20):
    #     client.publish("Damkar", str(i))
    #     time.sleep(1)