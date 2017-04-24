import cv2
import numpy as np
from queue import Queue

cap = cv2.VideoCapture('C:\\Users\\Henchiri\\Downloads\\Video\\170406-020248.mpg')

boundaries = [
	#([0, 0, 240], [10, 10, 255]),
	([240, 0, 0], [255, 10, 10]),
	([0, 240, 0], [10, 255, 10])
]


myQueue = Queue()
paddle_position = 0 
pong_position = 0

while True:
	(grabbed, frame) = cap.read()
	#print(grabbed)
	if not grabbed:
		break



	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
	
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(frame, lower, upper)
		output = cv2.bitwise_and(frame, frame, mask = mask)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
		if len(cnts) > 0:
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			print(center)
			#print(center[0])
			#print(center[1])
			myQueue.put(center[1])
	
	paddle_position = myQueue.get()
	myQueue.task_done()
	pong_position = myQueue.get()
	myQueue.task_done()

	if(paddle_position < pong_position):
		print(-1)
	elif(paddle_position > pong_position):
		print(1)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()