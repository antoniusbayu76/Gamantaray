import time
import paho.mqtt.client as paho

Broker = "10.73.162.88"

def on_message(client, userdata, message):
    #print("topik",message.topic)
    #print("data", str(message.payload.decode("utf-8"))) 
    sumber = message.topic
    isi = str(message.payload.decode("utf-8"))
    #if (sumber == "Keselamatan") and (isi == "kobong"):
        #client.publish("Damkar", berangkat)
        #print(sumber, isi)
    #if (sumber == "Keselamatan") and (isi == "Selamat"):
        #client.publish("Damkar", selesai)
        #print(sumber, isi)

    if (sumber == "Foodstall"):
        
        print(sumber, isi)

berangkat = "Bomba datang"
selesai = "semua kami selamatkan"
coba = ['U', 'UD', 'UDI', 'UDIN', 'UDIN ', 'UDIN A', 'UDIN AY', 'UDIN AYO', 'UDIN AYO ', 'UDIN AYO C', 'UDIN AYO CO', 'UDIN AYO COB', 'UDIN AYO COBA']
b = ['C', 'CA', 'CAP', 'CAPE', 'CAPEK', 'CAPEK ', 'CAPEK D', 'CAPEK DA', 'CAPEK DAH']
pulang = ['P', 'PE', 'PEN', 'PENG', 'PENGE', 'PENGEN', 'PENGEN ', 'PENGEN P', 'PENGEN PU', 'PENGEN PUL', 'PENGEN PULA', 'PENGEN PULAN', 'PENGEN PULANG']
kasian = ['G', 'GA', 'GAK', 'GAK ', 'GAK P', 'GAK PU', 'GAK PUN', 'GAK PUNY', 'GAK PUNYA', 'GAK PUNYA T', 'GAK PUNYA TE', 'GAK PUNYA TEM', 'GAK PUNYA TEME', 'GAK PUNYA TEMEN']
sendiri = ['S', 'SE', 'SEN', 'SEND', 'SENDI', 'SENDIR', 'SENDIRI', 'SENDIRIA', 'SENDIRIAN']
client = paho.Client("Ayo")
#client.on_message=on_message
client.connect(Broker)
client.loop_start()
while(True):
    client.on_message=on_message
    client.subscribe("Foodstall")
    time.sleep(0.3)  
client.loop_stop()
client.disconnect()