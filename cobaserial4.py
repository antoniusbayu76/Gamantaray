import serial
import time
ser = serial.Serial('COM4',9600)

x=0

while True :
    print("bisa")

    if(x%2==0):
        ser.write("on".encode('utf-8'))
        print("on")
    elif(x%2!=0):
        ser.write("off".encode('utf-8'))
        print("off")
    x+=1
    time.sleep(1)
    if(x>30):
        exit()
