import cv2
import numpy as np
import time

#---------Inisiasi---------# 


#List masking hijau
listLowGreen = [np.array([92, 66, 97 ])] #[np.array([83, 28, 101])] 
listUpGreen = [np.array([98, 240, 255])] #[np.array([94, 116, 158])] 
nGreen = 0

 

batasLuasAtasHijau = 10000
batasLuasBawahHijau = 500   

setpoin = 5000

asalVideo = 0#'/home/gamantaray/Videos/Webcam/video.mp4' #0#D:\Resources/raw.mp4
path = 1
scaling = 0.3


count = 0
delay = 1


#--------------------------#




##Fungsi rescale
def rescale(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width,height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def bolahijau(img,hsv,upper,lower):
    global maskGreen
    maskGreen = cv2.inRange(hsv, lower, upper)
    return cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)






##Ambil file video
capture = cv2.VideoCapture(asalVideo)
cap = cv2.VideoCapture(path)
global flag
global cek
flag = 0
cek = 0


while True:
    ##Ambil frame video
    status, img = capture.read()
    status, img2 = cap.read()

    img = rescale(img, scaling) 
    img2 = rescale(img2,0.2)
    img2 = cv2.rotate(img2 ,cv2.ROTATE_180)
    #print(img.shape[1],img.shape[0])
    
    ##Image processing(blurring)
    frame = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
   
    
    ##Image processing(seleksi warna & masking)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    
    #Pengolahan Bola HIjau
    contours2, hierarchy =  bolahijau(img,hsv,listUpGreen[nGreen],listLowGreen[nGreen])




    contoursList2 = []
    for i in contours2:
        area2 = cv2.contourArea(i)
        #print('Luas Hijau =',area)  ##Green Area Check##

        if area2 < batasLuasAtasHijau and area2 > batasLuasBawahHijau:
            contoursList2.append(i)
            

    contours2 = tuple(contoursList2)
    # print(nRed)
    

    ##Image segmenting HIJAU (KANAN)
    if len(contours2) > 0:
        c = max(contours2, key=cv2.contourArea)
        
        area2 = cv2.contourArea(c)
        # print('maxHIJAU=',area2)
        
        M = cv2.moments(c)
        if M['m00']!=0:
            cxH = int(M['m10']/M['m00'])
            cyH = int(M['m01']/M['m00'])
            cv2.rectangle(img, (cxH-20,cyH-20), (cxH+20,cyH+20), (0,255,0), 1)
        # cv2.putText(img, "Luas = "+str(area2), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if area2 > setpoin :
            image_name = "mangrove{}.png".format(count)
            cv2.imwrite(image_name,img)
            image_name2 = "ikan{}.png".format(count)
            cv2.imwrite(image_name2,img2)
            count = count + 1

    else:
            cxH = img.shape[1]+5
            cyH = img.shape[0]//2+10
            #pindah masking hijau
            nGreen += 1

            if nGreen == len(listLowGreen) :
                nGreen = 0
    # cv2.drawContours(img, contours2, -1, (255,255,255),1)
        
           
    # print(len(contours))
    ##Menampilkan

    cv2.imshow('raw image', img)
    cv2.imshow('bawah', img2)

    # cv2.imshow('merah', maskRed)
    # cv2.imshow('hijau', maskGreen)
    # cv2.imshow('hsv', hsv)
    # cv2.imshow('result', result)
    # cv2.imshow('resultp', maskFinal)
    # time.sleep(0.01)


    if cv2.waitKey(1) == ord('q'):
        break
        



capture.release()
cv2.destroyAllWindows()
