import time
import paho.mqtt.client as paho

broker = "10.73.14.99"
port = 1883

def on_message(client, userdata, message):
    
    sumber = message.topic
    isi = str(message.payload.decode("utf-8"))
    
    if (sumber == "SPBU"):
        print(sumber, isi)


# MQTT
Broker = broker
client = paho.Client("LaptopYahya")
client.connect(Broker,port)
# client.loop_start()
print('publish oke')

while(True):
    # client.on_message=on_message
    client.publish("SPBU","a")
    print("publish a")
    time.sleep(1)
    # client.subscribe("SPBU")
    # print("done")

    # for i in range(20):
    #     client.publish("Damkar", str(i))
    #     time.sleep(1)