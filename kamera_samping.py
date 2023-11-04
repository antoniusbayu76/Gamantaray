import cv2
import numpy as np
import serial
import time


#---------Inisiasi---------# 
INVERS = 'n' #(y/n)


#List masking merah
listLowRed = [np.array([0,26,53]),np.array([163,43,142]),np.array([0,81,127])] # [np.array([0, 111, 109])]
listUpRed = [np.array([7,255,168]),np.array([180,255,255]),np.array([4,244,249])] #[np.array([3, 190, 178])] 
nRed = 0

#List masking hijau
listLowGreen = [np.array([70,145,24]),np.array([76, 121, 17 ]), np.array([62,147,0])] #[np.array([83, 28, 101])] 
listUpGreen = [np.array([83,255,89]),np.array([97, 255, 255]),np.array([179, 255, 255])] #[np.array([94, 116, 158])] 
nGreen = 0



batasLuasAtasMerah = 10000  
batasLuasBawahMerah = 200  

batasLuasAtasHijau = 3000
batasLuasBawahHijau = 200   


port = '/dev/ttyUSB0'  #############################
bautRate = 9600

asalVideo = 'D:\Resources/raw.mp4'
scaling = 1

areaLurus = 20
areaBelokTipis = 40
areaBelokBesar = 40

blockAtas = 200
blockTengah = 120
blockKanan = 105
blockKiri = 105
blockBawah = 90
segitigaVertikal = 180
segitigaHorizontal = 160

count = 0


#--------------------------#



##Koordinat area manuver
batasLurus = {
    "+"     : areaLurus,
    "-"     : -areaLurus,
}

batasBelokTipis = {
    "+kanan"    : (areaLurus + areaBelokTipis),
    "+kiri"     : (areaLurus) -1,
    
    "-kanan"    : -(areaLurus) +1,
    "-kiri"     : -(areaLurus + areaBelokTipis),
}

batasBelokBesar = {
    "+kanan"    : (areaLurus + areaBelokTipis + areaBelokBesar),
    "+kiri"     : (areaLurus + areaBelokTipis) -1,

    "-kanan"    : -(areaLurus + areaBelokTipis) +1,
    "-kiri"     : -(areaLurus + areaBelokTipis + areaBelokBesar),
}

##Balik bola kanan sama kiri
if INVERS == 'y':

    listLowRed2 = listLowRed
    listUpRed2 = listUpRed

    listLowRed = listLowGreen
    listUpRed = listUpGreen
    listLowGreen = listLowRed2
    listUpGreen = listUpRed2


    batasLuasAtasMerah2 = batasLuasAtasMerah
    batasLuasBawahMerah2 = batasLuasBawahMerah

    batasLuasAtasMerah = batasLuasAtasHijau
    batasLuasBawahMerah = batasLuasBawahHijau
    batasLuasAtasHijau = batasLuasAtasMerah2
    batasLuasBawahHijau = batasLuasBawahMerah2

    ################################

##Fungsi rescale
def rescale(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width,height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

#Fungsi Pengolahan Citra
def bolamerah(img,hsv,upper,lower):
    global maskRed
    maskRed = cv2.inRange(hsv, lower, upper)
    return cv2.findContours(maskRed,1,cv2.CHAIN_APPROX_NONE)
    
def bolahijau(img,hsv,upper,lower):
    global maskGreen
    maskGreen = cv2.inRange(hsv, lower, upper)
    return cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)




##Nyambungin ke arduino
try:
    ser = serial.Serial(port, bautRate, timeout=None)
    arduino = 'ada'
    #startNyelem = 1000
except:
    arduino = 'gada'
    print('------------gada arduino------------')




##Ambil file video
capture = cv2.VideoCapture(asalVideo)


while True:
    ##Ambil frame video
    status, img = capture.read()


    img = rescale(img, scaling) 
    #print(img.shape[1],img.shape[0])
    # cv2.rectangle(img, (0,0), (img.shape[1],blockAtas), (0,0,0), thickness=-1)
    # cv2.rectangle(img, (img.shape[1]//2,0), (img.shape[1],img.shape[0]), (0,0,0), thickness=-1)
    
    ##Image processing(blurring)
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
        # print('Luas kIRI =',area1)  ##Red Area Checking##

        if area1 < batasLuasAtasMerah and area1 > batasLuasBawahMerah:
            contoursList.append(i)
            
            

    contours = tuple(contoursList)


    contoursList2 = []
    for i in contours2:
        area2 = cv2.contourArea(i)
        #print('Luas Hijau =',area)  ##Green Area Check##

        if area2 < batasLuasAtasHijau and area2 > batasLuasBawahHijau:
            contoursList2.append(i)
            

    contours2 = tuple(contoursList2)

    ##Image segmenting MERAH (KIRI)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        
        area1 = cv2.contourArea(c)
        #print('maxKIRI=',area)
        
        M = cv2.moments(c)
        if M['m00']!=0:
            cxM = int(M['m10']/M['m00'])
            cyM = int(M['m01']/M['m00'])
            cv2.rectangle(img, (cxM-50,cyM-50), (cxM+50,cyM+50), (255,255,255), 1)

    else:
            cxM = -5
            cyM = img.shape[0]//2+10
            #pindah masking merah
            nRed += 1
            if nRed == len(listLowRed) :
                nRed = 0

    cv2.drawContours(img, contours, -1, (255,255,255),1)
    # print(nRed)



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

    else:
            cxH = img.shape[1]+5
            cyH = img.shape[0]//2+10
            #pindah masking hijau
            nGreen += 1
            if nGreen == len(listLowGreen) :
                nGreen = 0
    cv2.drawContours(img, contours2, -1, (255,255,255),1)


    if len(contours) > 0 and len(contours2) > 0 :
        ser.write('a'.encode())
        print("kiri")

    if len(contours) < 1 and len(contours2) > 0 :
        cv2.putText(frame, "Luas = "+str(area2), (cxH-53,cyH-53), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    



    ##Menampilkan
    cv2.imshow('raw image', img)
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
