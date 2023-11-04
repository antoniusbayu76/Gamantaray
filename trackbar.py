import cv2
import numpy as np

def empty(a):
    pass

path = 'C:/Users/Lenovo/Pictures/Camera Roll/WIN_20230909_08_04_47_Pro.jpg'
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",159,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",179,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",45,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",148,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

cv2.namedWindow("TrackBars2")
cv2.resizeWindow("TrackBars2",640,240)
cv2.createTrackbar("Hue Min2","TrackBars2",73,179,empty)
cv2.createTrackbar("Hue Max2","TrackBars2",96,179,empty)
cv2.createTrackbar("Sat Min2","TrackBars2",49,255,empty)
cv2.createTrackbar("Sat Max2","TrackBars2",255,255,empty)
cv2.createTrackbar("Val Min2","TrackBars2",50,255,empty)
cv2.createTrackbar("Val Max2","TrackBars2",255,255,empty)

while True:
    img = cv2.imread(path)
    blur = cv2.GaussianBlur(img,(31,31),cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    h_min2 = cv2.getTrackbarPos("Hue Min2", "TrackBars2")
    h_max2 = cv2.getTrackbarPos("Hue Max2", "TrackBars2")
    s_min2 = cv2.getTrackbarPos("Sat Min2", "TrackBars2")
    s_max2 = cv2.getTrackbarPos("Sat Max2", "TrackBars2")
    v_min2 = cv2.getTrackbarPos("Val Min2", "TrackBars2")
    v_max2 = cv2.getTrackbarPos("Val Max2", "TrackBars2")

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max, s_max, v_max])

    lower2 = np.array([h_min2,s_min2,v_min2])
    upper2 = np.array([h_max2, s_max2, v_max2])


    mask_merah = cv2.inRange(hsv,lower,upper)
    mask_hijau = cv2.inRange(hsv,lower2,upper2)

    result = cv2.bitwise_or(mask_hijau, mask_merah)
    result = cv2.bitwise_and(img, img, mask= result)

    cv2.imshow("HSV",mask_hijau)
    cv2.imshow("HSV2",mask_merah)
    cv2.imshow("ImgResult", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
            break

  
cv2.destroyAllWindows()