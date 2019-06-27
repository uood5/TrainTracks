# Written by Seth Woolley
# Code for getting puzzle area can be found here:
# https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/

from imutils.perspective import four_point_transform
from imutils import contours
import sys, cv2, imutils

image = cv2.imread(sys.argv[1])

image=imutils.resize(image, height=550)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)

# find contours in the edge map, then sort them by their
# size in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

displayCnt = [] 
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if the contour has four vertices, then we have found
	# the thermostat display
	if len(approx) == 4:
		displayCnt = approx
		break

if displayCnt == []:
	print("No puzzle found, try another image")
	sys.exit()

# extract the puzzle, apply a perspective transform to it
warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4, 2))

cv2.imshow("warped",warped)
cv2.imshow("output",output)
cv2.imshow("warped edges",cv2.Canny(warped,50,200,255))
cv2.waitKey(0) 