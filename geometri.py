import cv2

cap1 = cv2.VideoCapture(0)


while True :
    status, img = cap1.read()

    imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #daidiahodqho

    ret , thrash = cv2.threshold(imgGry, 130 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)



    for contour in contours:
        area = cv2.contourArea(contour)
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        if area > 800  :
            
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            if len(approx) == 3:
                cv2.putText( img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )
            elif len(approx) == 4 :
                x, y , w, h = cv2.boundingRect(approx)
                aspectRatio = float(w)/h
                cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            elif len(approx) == 5 :
                cv2.putText(img, "pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 10 :
                cv2.putText(img, "star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            # else:
            #     cv2.putText(img, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    


    cv2.imshow('raw image1', img)
    cv2.imshow('trash', thrash)
    cv2.imshow('grey', imgGry)


    if cv2.waitKey(1) == ord('q'):
        break
        

cap1.release()
cv2.destroyAllWindows()
