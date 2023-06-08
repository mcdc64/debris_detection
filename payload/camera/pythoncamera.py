import cv2

cam = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)

while True:
	ret, image = cam.read()
	ret2, image2 = cam2.read()
	cv2.imshow('Imagetest',image)
	cv2.imshow('Imagetest2',image2)
	k = cv2.waitKey(1)
	if k != -1:
		break
cv2.imwrite('/home/pi/testimage.jpg', image)
cv2.imwrite('/home/pi/testimage2.jpg', image2)

cam.release()
cv2.destroyAllWindows()
