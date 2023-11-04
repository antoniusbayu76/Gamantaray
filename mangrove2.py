import cv2
import numpy as np
import serial


# listLowGreen = [np.array([73, 49, 50 ])]
# listUpGreen = [np.array([96, 255, 255 ])]
listLowGreen = [np.array([76, 121, 17 ]), np.array([62,147,0])]
listUpGreen = [np.array([97, 255, 255]),np.array([179, 255, 255])]
nGreen = 0

#inisiasi arduino
port = '/dev/ttyUSB0'  
bautRate = 9600

batasLuasAtasHijau = 20000
batasLuasBawahHijau = 400 

area = 0
setpoint = 1000
count = 1
path = 'D:\Resources/Copy of WIN_20221027_17_04_03_Pro.mp4'
scaling = 0.5

cap = cv2.VideoCapture(path)
flag = False

try:
    ser = serial.Serial(port, bautRate, timeout=None)
    arduino = 'ada'
    #startNyelem = 1000
except:
    arduino = 'gada'
    print('------------gada arduino------------')

    
def mangrove(img,hsv,upper,lower):
    global maskGreen
    maskGreen = cv2.inRange(hsv, lower, upper)
    # cv2.rectangle(maskGreen, (0,0), (img.shape[1]//5,img.shape[0]), (0,0,0), thickness=-1) ###
    return cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)

def rescale(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width,height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

while True :
    status, img = cap.read()
    img = rescale(img, scaling) 
    frame = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
    
    
    ##Image processing(seleksi warna & masking)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Pengolahan Bola HIjau
    contours, hierarchy =  mangrove(img,hsv,listUpGreen[nGreen],listLowGreen[nGreen])

    ##Seleksi luas HIJAU (KANAN)
    # contours, hierarchy = cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)

    contourList = []
    for i in contours:
        area = cv2.contourArea(i)
        #print('Luas Hijau =',area)  ##Green Area Check##

        if area < batasLuasAtasHijau and area > batasLuasBawahHijau:
            contourList.append(i)
            

    contours = tuple(contourList)


    ##Image segmenting HIJAU (KANAN)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        
        area = cv2.contourArea(c)
        #qprint('maxHIJAU=',area)
        
        M = cv2.moments(c)
        if M['m00']!=0:
            cxH = int(M['m10']/M['m00'])
            cyH = int(M['m01']/M['m00'])
            cv2.rectangle(img, (cxH-20,cyH-20), (cxH+20,cyH+20), (255,255,255), 1)

    else:
            cxH = img.shape[1]+5
            cyH = img.shape[0]//2+10
            #pindah masking hijau
            nGreen += 1
            if nGreen == len(listLowGreen) :
                nGreen = 0
    cv2.drawContours(maskGreen, contours, -1, (255,255,255),1)
    cv2.putText(img,"Luas = "+str(area) , (0, img.shape[0]), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0,0,255), thickness=1)

    # k = cv2.waitKey(1)
    
    # if area > setpoint:
    #     flag = True

    # if flag == True :
    #     if count % 3 == 0 :
    #         img_name ="img{}.png".format(count)
    #         cv2.imwrite(img_name,img)
    #     count = count + 1
    if arduino == 'ada' :
        if area < setpoint:
            ser.write('e'.encode())
            print('belok kiri')

        else :
            ser.write('a'.encode())
            print('lurus')



    


    cv2.imshow('raw image', img)
    # cv2.imshow('hsv image', hsv)
    # cv2.imshow('result image', result)
    # cv2.imshow('merah image', maskRed)
    cv2.imshow('hijau image', maskGreen)

    if cv2.waitKey(1) == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()