import cv2
import numpy as np


listlowYellow = [np.array([24, 84, 52 ])]#,np.array([76, 121, 17 ]), np.array([62,147,0])]
listupYellow = [np.array([30, 177, 255 ])]#, np.array([97, 255, 255]),np.array([179, 255, 255])]
nGreen = 0

batasLuasAtasHijau = 20000
batasLuasBawahHijau = 400 

area2 = 0
count = 10

cap = cv2.VideoCapture(1)

    
def bolahijau(img,hsv,upper,lower):
    global maskGreen
    maskGreen = cv2.inRange(hsv, lower, upper)
    # cv2.rectangle(maskGreen, (0,0), (img.shape[1]//5,img.shape[0]), (0,0,0), thickness=-1) ###
    return cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)

while True :
    status, img = cap.read()

    frame = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
   
    
    ##Image processing(seleksi warna & masking)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    #Pengolahan Bola HIjau
    contours2, hierarchy =  bolahijau(img,hsv,listupYellow[nGreen],listlowYellow[nGreen])

    

    contoursList2 = []
    for i in contours2:
        area2 = cv2.contourArea(i)
        #print('Luas Hijau =',area)  ##Green Area Check##

        if area2 < batasLuasAtasHijau and area2 > batasLuasBawahHijau:
            contoursList2.append(i)
            

    contours2 = tuple(contoursList2)


    ##Image segmenting HIJAU (KANAN)
    if len(contours2) > 0:
        c = max(contours2, key=cv2.contourArea)
        
        area2 = cv2.contourArea(c)
        #qprint('maxHIJAU=',area2)
        
        M = cv2.moments(c)
        if M['m00']!=0:
            cxH = int(M['m10']/M['m00'])
            cyH = int(M['m01']/M['m00'])
            cv2.rectangle(img, (cxH-50,cyH-50), (cxH+50,cyH+50), (255,255,255), 1)
        cv2.line(img, (cxH,0), (cxH,img.shape[0]), (0,255,0), thickness=2)

    else:
            # cxH = img.shape[1]+5
            # cyH = img.shape[0]//2+10
            #pindah masking hijau
            nGreen += 1
            if nGreen == len(listlowYellow) :
                nGreen = 0
    cv2.drawContours(maskGreen, contours2, -1, (255,255,255),1)
    cv2.putText(img,"Luas = "+str(area2) , (0, img.shape[0]), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0,0,255), thickness=1)
   
    cv2.line(img, (0,img.shape[0]//2), (img.shape[1],img.shape[0]//2), (255,255,255), thickness=2)
    cxDOT = img.shape[1] // 2
    cyDOT = img.shape[0] // 2
    cv2.circle(img, (cxDOT,cyDOT), 10, (0,0,0), thickness=2)


    


    cv2.imshow('raw image', img)
    # cv2.imshow('hsv image', hsv)
    # cv2.imshow('result image', result)
    # cv2.imshow('merah image', maskRed)
    cv2.imshow('hijau image', maskGreen)

    if cv2.waitKey(1) == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()