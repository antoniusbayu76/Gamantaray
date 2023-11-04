import cv2
import numpy as np
import serial
import time


#---------Inisiasi---------# 
INVERS = 'n' #(y/n)

lowerRed = np.array([163,43,142])  #[0, 124, 53]     #[163,43,142]
upperRed = np.array([180,255,255]) #[74, 255, 255]   #[180,255,255]
lowerRed2 = np.array([0, 124, 53])  
upperRed2 = np.array([74, 255, 255])

lowerGreen = np.array([79, 221, 0 ])  #TRIAL 1 : 79 221 0        #[84,97,0]                       #76 121 17  #66 57 0
upperGreen = np.array([95, 255, 255]) #TRIAL 1 : 93 255 255    #[95,255,255]                      #97 255 255  #102 255 255
lowerGreen2 = np.array([84,97,0])  
upperGreen2 = np.array([93, 255, 255])



batasLuasAtasMerah = 900  
batasLuasBawahMerah = 200  

batasLuasAtasHijau = 1000  
batasLuasBawahHijau = 200   


port = '/dev/ttyACM0'  #############################
bautRate = 2000000

asalVideo = 'D:\Resources/Copy of WIN_20221027_17_04_03_Pro.mp4'
scaling = 0.5

areaLurus = 20
areaBelokTipis = 25
areaBelokBesar = 20

blockAtas = 200
blockTengah = 120
blockKanan = 105
blockKiri = 105
blockBawah = 90
segitigaVertikal = 180
segitigaHorizontal = 160


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
    lowerRed2 = lowerRed
    upperRed2 = upperRed

    lowerRed = lowerGreen
    upperRed = upperGreen
    lowerGreen = lowerRed2
    upperGreen = upperRed2


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
    

    ##Area of interest
    cv2.rectangle(img, (0,0), (img.shape[1],blockAtas), (0,0,0), thickness=-1)  #y=90  #y=110   ###
    cv2.rectangle(img, ((img.shape[1]//2)-blockTengah,0), ((img.shape[1]//2)+blockTengah,img.shape[0]), (0,0,0), thickness=-1) ###
    cv2.line(img, (img.shape[1]//5,blockAtas-30), (-5,blockAtas+20), (0,0,0), thickness=blockKiri) ###
    cv2.line(img, (img.shape[1]-img.shape[1]//5,blockAtas-30), (img.shape[1]+5,blockAtas+20), (0,0,0), thickness=blockKanan) ###
   #------------------------------------------------------------------------------------------------------------ 
   #roi tambahan
    cv2.rectangle(img, (0,(img.shape[0]//2)+blockBawah), (img.shape[1],img.shape[0]), (0,0,0), thickness=-1)
    points = np.array([[120+segitigaHorizontal, 180+segitigaVertikal], [200+segitigaHorizontal, 110+segitigaVertikal], [200+segitigaHorizontal, 180+segitigaVertikal]]) 
    cv2.fillPoly(img, pts=[points], color=(255, 0, 0))#merah
    points2 = np.array([[540+segitigaHorizontal, 180+segitigaVertikal], [440+segitigaHorizontal, 110+segitigaVertikal], [440+segitigaHorizontal, 180+segitigaVertikal]])
    cv2.fillPoly(img, pts=[points2], color=(255, 0, 0))#hijau




    ##Image processing(blurring)
    frame = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
   
    
    ##Image processing(seleksi warna & masking)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maskRed = cv2.inRange(hsv, lowerRed, upperRed)
    maskGreen = cv2.inRange(hsv, lowerGreen, upperGreen)
    maskFinal = cv2.bitwise_or(maskRed, maskGreen)

    result = cv2.bitwise_and(img, img, mask= maskFinal)




    ##Area of interest (ngeblock setengah2 layar)
    cv2.rectangle(maskRed, (img.shape[1]//2,0), (img.shape[1],img.shape[0]), (0,0,0), thickness=-1) ###
    cv2.rectangle(maskGreen, (0,0), (img.shape[1]//2,img.shape[0]), (0,0,0), thickness=-1) ###
   

    
    ##Seleksi luas MERAH (KIRI)
    contours, hierarchy = cv2.findContours(maskRed,1,cv2.CHAIN_APPROX_NONE)

    contoursList = []
    for i in contours:
        area = cv2.contourArea(i)
        print('Luas kIRI =',area)  ##Red Area Checking##

        if area < batasLuasAtasMerah and area > batasLuasBawahMerah:
            contoursList.append(i)
        else : #pindah masking
            maskRed = cv2.inRange(hsv, lowerRed2, upperRed2)
            cv2.rectangle(maskRed, (img.shape[1]//2,0), (img.shape[1],img.shape[0]), (0,0,0), thickness=-1)
            contours, hierarchy = cv2.findContours(maskRed,1,cv2.CHAIN_APPROX_NONE)
            for i in contours:
                area = cv2.contourArea(i)
                #print('Luas kIRI =',area)  ##Red Area Checking##

                if area < batasLuasAtasMerah and area > batasLuasBawahMerah:
                    contoursList.append(i)
            
            

    contours = tuple(contoursList)


    ##Image segmenting MERAH (KIRI)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        
        area = cv2.contourArea(c)
        #print('maxKIRI=',area)
        
        M = cv2.moments(c)
        if M['m00']!=0:
            cxM = int(M['m10']/M['m00'])
            cyM = int(M['m01']/M['m00'])
            cv2.rectangle(result, (cxM-20,cyM-20), (cxM+20,cyM+20), (255,255,255), 1)

    else:
            cxM = -5
            cyM = img.shape[0]//2+10
    cv2.drawContours(result, contours, -1, (255,255,255),1)



    ##Seleksi luas HIJAU (KANAN)
    contours, hierarchy = cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)

    contoursList = []
    for i in contours:
        area = cv2.contourArea(i)
        #print('Luas Hijau =',area)  ##Green Area Check##

        if area < batasLuasAtasHijau and area > batasLuasBawahHijau:
            contoursList.append(i)
        else : #pindah masking
            maskGreen = cv2.inRange(hsv, lowerGreen2, upperGreen2)
            cv2.rectangle(maskGreen, (0,0), (img.shape[1]//2,img.shape[0]), (0,0,0), thickness=-1)
            contours, hierarchy = cv2.findContours(maskGreen,1,cv2.CHAIN_APPROX_NONE)
            for i in contours:
                area = cv2.contourArea(i)
                #print('Luas kIRI =',area)  ##Red Area Checking##

                if area < batasLuasAtasHijau and area > batasLuasBawahHijau:
                    contoursList.append(i)
            

    contours = tuple(contoursList)


    ##Image segmenting HIJAU (KANAN)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        
        area = cv2.contourArea(c)
        print('maxHIJAU=',area)
        
        M = cv2.moments(c)
        if M['m00']!=0:
            cxH = int(M['m10']/M['m00'])
            cyH = int(M['m01']/M['m00'])
            cv2.rectangle(result, (cxH-20,cyH-20), (cxH+20,cyH+20), (255,255,255), 1)

    else:
            cxH = img.shape[1]+5
            cyH = img.shape[0]//2+10
    cv2.drawContours(result, contours, -1, (255,255,255),1)


    ##Garis & lingkaran tengah
    cv2.line(result, (img.shape[1]//2,0), (img.shape[1]//2,img.shape[0]), (0,255,255), thickness=2) ###
    cv2.line(result, (cxM,cyM), (cxH,cyH), (255,255,255), thickness=2)
    cxDOT = (cxH + cxM) // 2
    cyDOT = (cyH + cyM) // 2
    cv2.circle(result, (cxDOT,cyDOT), 10, (0,255,255), thickness=2)

    ##Area - area manuver kapal
    cv2.line(result, (img.shape[1]//2 + batasLurus['-'], 0), (img.shape[1]//2 + batasLurus['-'],img.shape[0]), (255,255,255), thickness=1) ###
    cv2.line(result, (img.shape[1]//2 + batasLurus['+'],0), (img.shape[1]//2 + batasLurus['+'],img.shape[0]), (255,255,255), thickness=1) ###
    cv2.putText(result, 'a', (img.shape[1]//2,img.shape[0]-20), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255,255,255), thickness=1) ###

    cv2.line(result, (img.shape[1]//2 + batasBelokTipis['-kiri'], 0), (img.shape[1]//2 + batasBelokTipis['-kiri'],img.shape[0]), (255,255,255), thickness=1) ###
    cv2.line(result, (img.shape[1]//2 + batasBelokTipis['+kanan'],0), (img.shape[1]//2 + batasBelokTipis['+kanan'],img.shape[0]), (255,255,255), thickness=1) ###
    cv2.putText(result, 'b', (img.shape[1]//2 + ((batasBelokTipis['-kiri']+batasLurus['-'])//2) , img.shape[0]-20), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255,255,255), thickness=1) ###
    cv2.putText(result, 'c', (img.shape[1]//2 + ((batasBelokTipis['+kanan']+batasLurus['+'])//2) , img.shape[0]-20), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255,255,255), thickness=1) ###

    cv2.line(result, (img.shape[1]//2 + batasBelokBesar['-kiri'], 0), (img.shape[1]//2 + batasBelokBesar['-kiri'],img.shape[0]), (255,255,255), thickness=1) ###
    cv2.line(result, (img.shape[1]//2 + batasBelokBesar['+kanan'],0), (img.shape[1]//2 + batasBelokBesar['+kanan'],img.shape[0]), (255,255,255), thickness=1) ###
    cv2.putText(result, 'd', (img.shape[1]//2 + ((batasBelokBesar['-kiri']+batasBelokTipis['-kiri'])//2) , img.shape[0]-20), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255,255,255), thickness=1) ###
    cv2.putText(result, 'e', (img.shape[1]//2 + ((batasBelokBesar['+kanan']+batasBelokTipis['+kanan'])//2) , img.shape[0]-20), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255,255,255), thickness=1) ###


    ##jarak sumbu x lingkaran, ke tengah
    cx = cxDOT - img.shape[1]/2
    #print(cx)


    ##Menampilkan
    cv2.imshow('raw image', img)
    cv2.imshow('result', result)
    cv2.imshow('results', maskRed)
    time.sleep(0.05)


    ##Ngirim data ke arduino
    if arduino == 'ada':

        ##Lurus
        if cx > batasLurus['-'] and cx < batasLurus['+']:
            ser.write('a'.encode())
            print('a')
        

        ##Belok kiri tipis
        elif cx > batasBelokTipis["-kiri"] and cx < batasBelokTipis["-kanan"]:
            ser.write('b'.encode())

            print('b')
        ##Belok kanan tipis
        elif cx > batasBelokTipis["+kiri"] and cx < batasBelokTipis["+kanan"]:
            ser.write('c'.encode())

            print('c')


        ##Belok kiri besar
        elif cx > batasBelokBesar['-kiri'] and cx < batasBelokBesar['-kanan']:
            ser.write('d'.encode())

            print('d')
        ##Belok kanan besar
        elif cx > batasBelokBesar['+kiri'] and cx < batasBelokBesar['+kanan']:
            ser.write('e'.encode())

            print('e')


        ##Belok kiri tajam
        elif cx < batasBelokBesar['-kiri']:
            ser.write('f'.encode())
            p = 'x'

            print('f')

            
        ##Belok kanan tajam
        elif cx > batasBelokBesar['+kanan']:
            ser.write('g'.encode())
            p = 'x'

            print('g')






    if cv2.waitKey(1) == ord('q'):
        break
        



capture.release()
cv2.destroyAllWindows()
