import cv2

# Run the other script


cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
cap3 = cv2.VideoCapture(0)

count = 0

# main.py



while True :
    status, img1 = cap3.read()
    # status, img2 = cap2.read()
    # status, img3 = cap3.read()

    k = cv2.waitKey(1)

    if k%256 == 32:
        img_name ="img{}.png".format(count)
        cv2.imwrite(img_name,img1)
        count += 1
    
  

    cv2.imshow('raw image3', img1)
    # cv2.imshow('raw image2', img2)
    # cv2.imshow('raw image3', img3)

    if cv2.waitKey(1) == ord('q'):
        break
        




cap2.release()
# cap3.release()
cv2.destroyAllWindows()
