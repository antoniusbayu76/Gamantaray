# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(1)

while(True):
	
	ret, frame = vid.read()

	# Display the resulting frame
	cv2.imshow('frame', frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


vid.release()
cv2.destroyAllWindows()
