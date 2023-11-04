import serial
import time
import struct
ser = serial.Serial('COM4',9600)

x=0

while True :
    print("bisa")

    if(x%2==0):
        ser.write(struct.pack('>B',1))
        print('1')
    elif(x%2!=0):
        ser.write(struct.pack('>B',2))
        print('2')
    x+=1
    time.sleep(1.5)
    if(x>30):
        exit()
