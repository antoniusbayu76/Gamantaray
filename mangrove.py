import cv2
import numpy as np

listLowRed = [np.array([163,43,142]),np.array([0, 78, 67])]
listUpRed = [np.array([180,255,255]),np.array([6, 255, 177])]
nRed = 0

listLowGreen = [np.array([76, 121, 17 ]), np.array([62,147,0])]
listUpGreen = [np.array([97, 255, 255]),np.array([179, 255, 255])]
nGreen = 0

batasLuasAtasMerah = 10000  
batasLuasBawahMerah = 200  

batasLuasAtasHijau = 10000
batasLuasBawahHijau = 200 

garisM = 150
garisH = 150

cap = cv2.VideoCapture(1)

def bolamerah(img,hsv,upper,lower):
    global maskRed
    maskRed = cv2.inRange(hsv, lower, upper)
    cv2.rectangle(maskRed, (img.shape[1]*4//5,0), (img.shape[1],img.shape[0]), (0,0,0), thickness=-1)
    return cv2.findContours(maskRed,1,cv2.CHAIN_APPROX_NONE)
    
def bolahijau(img,hsv,upper,lower):
    global maskGreen
    maskGreen = cv2.inRange(hsv, lower, upper)
    cv2.rectangle(maskGreen, (0,0), (img.shape[1]//5,img.shape[0]), (0,0,0), thickness=-1) ###
    return cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)

while True :
    status, img = cap.read()

    frame = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
   
    
    ##Image processing(seleksi warna & masking)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Pengolahan Bola Merah
    contours,hierarchy = bolamerah(img,hsv,listUpRed[nRed],listLowRed[nRed])
    #Pengolahan Bola HIjau
    contours2, hierarchy =  bolahijau(img,hsv,listUpGreen[nGreen],listLowGreen[nGreen])

    
    maskFinal = cv2.bitwise_or(maskRed, maskGreen)
    result = cv2.bitwise_and(img, img, mask= maskFinal)


    contoursList = []
    for i in contours:
        area1 = cv2.contourArea(i)
        #print('Luas kIRI =',area1)  ##Red Area Checking##

        if area1 < batasLuasAtasMerah and area1 > batasLuasBawahMerah:
            contoursList.append(i)
            
            

    contours = tuple(contoursList)


    ##Image segmenting MERAH (KIRI)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        
        area1 = cv2.contourArea(c)
        #print('maxKIRI=',area)
        
        M = cv2.moments(c)
        if M['m00']!=0:
            cxM = int(M['m10']/M['m00'])
            cyM = int(M['m01']/M['m00'])
            cv2.rectangle(img, (cxM-20,cyM-20), (cxM+20,cyM+20), (255,255,255), 1)

    else:
            cxM = -5
            cyM = img.shape[0]//2+10
            #pindah masking merah
            nRed += 1
            if nRed == len(listLowRed) :
                nRed = 0

    cv2.drawContours(img, contours, -1, (255,255,255),1)
    

    ##Seleksi luas HIJAU (KANAN)
    # contours, hierarchy = cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)

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
            cv2.rectangle(img, (cxH-20,cyH-20), (cxH+20,cyH+20), (255,255,255), 1)

    else:
            cxH = img.shape[1]+5
            cyH = img.shape[0]//2+10
            #pindah masking hijau
            nGreen += 1
            if nGreen == len(listLowGreen) :
                nGreen = 0
    cv2.drawContours(img, contours2, -1, (255,255,255),1)


    cv2.line(img, (cxM+garisM,0), (cxM+garisM,img.shape[0]), (0,0,255), thickness=2)
    cv2.line(img, (cxM,0), (cxM,img.shape[0]), (0,0,255), thickness=2)
    cv2.line(img, (cxH,0), (cxH,img.shape[0]), (0,255,0), thickness=2)
    cv2.line(img, (cxH-garisH,0), (cxH-garisH,img.shape[0]), (0,255,0), thickness=2)
    cv2.line(img, (0,img.shape[0]//2), (img.shape[1],img.shape[0]//2), (255,255,255), thickness=2)
    cxDOT = img.shape[1] // 2
    cyDOT = img.shape[0] // 2
    cv2.circle(img, (cxDOT,cyDOT), 10, (0,0,0), thickness=2)
    


    cv2.imshow('raw image', img)
    # cv2.imshow('hsv image', hsv)
    cv2.imshow('result image', result)
    # cv2.imshow('merah image', maskRed)
    # cv2.imshow('hijau image', maskGreen)

    if cv2.waitKey(1) == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()