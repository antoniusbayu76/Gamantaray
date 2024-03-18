import cv2
import numpy as np
path = 1#"D:\Resources/raw.mp4"
cap = cv2.VideoCapture(path)

# upper = np.array([128, 192, 194])
# lower = np.array([43, 9, 61])
count = 1

while True:
    ##Ambil frame video
    status, img = cap.read()

    # frame = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
    img_name ="img{}.jpg".format(count)
    cv2.imwrite(img_name,img)
    count += 1

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