import cv2
import subprocess

# cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
# cap3 = cv2.VideoCapture(3)

while True :
    # status, img1 = cap1.read()
    status, img2 = cap2.read()
    newImg = cv2.rotate(img2, cv2.ROTATE_180)
    
    k = cv2.waitKey(1)
    # status, img3 = cap3.read()
    if k%256 == 27:
        cv2.destroyWindow('raw image2')
        cv2.destroyWindow('rotate image2')
        subprocess.run(["python", "multicamera3.py"])

    # cv2.imshow('raw image1', img1)q
    cv2.imshow('raw image2', img2)
    cv2.imshow('rotate image2', newImg)
    # cv2.imshow('raw image3', img3)

    if cv2.waitKey(1) == ord('q'):
        break
        



# cap1.release()
cap2.release()
# cap3.release()
cv2.destroyAllWindows()
