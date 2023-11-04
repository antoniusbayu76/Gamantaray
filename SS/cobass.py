import cv2
import numpy as np

cap = cv2.VideoCapture(0)

upper = np.array([128, 192, 194])
lower = np.array([43, 9, 61])
count = 0

while True:
    ##Ambil frame video
    status, img = cap.read()

    frame = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower,upper)
    contours,hierarchy = cv2.findContours(mask,1,cv2.CHAIN_APPROX_NONE)

    contoursList = []
    for i in contours:
        area1 = cv2.contourArea(i)
        #print('Luas kIRI =',area1)  ##Red Area Checking##

        if area1 > 500:
            contoursList.append(i)
            
    
    contours = tuple(contoursList)


    ##Image segmenting MERAH (KIRI)
    # if area1 > 100:
    #     count += 1
    #     if count >= 15 and count <=30:
    #         img_name ="img{}.png".format(count)
    #         cv2.imwrite(img_name,img)

    cv2.drawContours(img, contours, -1, (255,255,255),1)

    # k = cv2.waitKey(1)

    # if k%256 == 32:
    #     img_name ="img{}.png".format(count)
    #     cv2.imwrite(img_name,img)
    #     count =+ 1

    cv2.imshow('raw image', img)

    if cv2.waitKey(1) == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()