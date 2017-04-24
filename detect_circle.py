# import the necessary packages
import numpy as np
import argparse
import cv2

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread('C:\\Users\\Henchiri\\Downloads\\Video\\ScreenShot00086.png')
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

while  True:
	cv2.imshow('graty', gray)
	if cv2.waitKey(0):
		break

# detect circles in the image
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=20,minRadius=0,maxRadius=10)
print('before the loop')
 
# ensure at least some circles were found
if circles is not None:
	print('enter to the loop')
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	print(circles)
 
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
	# show the output image
	cv2.imshow("output", np.hstack([image, output]))
	cv2.waitKey(0)