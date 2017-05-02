# import the necessary packages
import numpy as np
import argparse
import cv2

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread('C:\\Users\\Henchiri\\Downloads\\Video\\ScreenShot00091.png')
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,0)
blured = cv2.GaussianBlur(gray,(5,5),0)


while  True:
	cv2.imshow('gray', thresh)
	if cv2.waitKey(0):
		break

# detect circles in the image
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,300,
                            param1=50,param2=20,minRadius=8,maxRadius=8)
 
# ensure at least some circles were found
if circles is not None:
	#print('enter to the loop')
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	print("circle coordinates = ",circles[0])


contours,hierarchy = cv2.findContours(thresh, 1, 2)[-2:] 
for cnt in contours:
    M = cv2.moments(cnt)
    if M['m00'] in range(650, 750):
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #print(M['m00'])
        print("paddle coordinates = ",center)   
