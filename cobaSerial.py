import serial
import cv2

port = '/dev/ttyACM0'
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=None)
    arduino = 'ada'
    #startNyelem = 1000
except:
    arduino = 'gada'
    print('------------gada arduino------------')
while True :
    if arduino == 'ada':
        ser.write('a')
        print('a')
 
    if cv2.waitKey(1) & 0xFF == ord("q"):
            break
