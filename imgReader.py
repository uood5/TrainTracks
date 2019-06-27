# Written by Seth Woolley
# Code for getting puzzle area can be found here:
# https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/

from imutils.perspective import four_point_transform
from imutils import contours
import sys, cv2, imutils
import numpy as np

image = cv2.imread(sys.argv[1])

image=imutils.resize(image, height=1000)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)

cv2.imshow("edged",edged)

# find contours in the edge map, then sort them by their
# size in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

rectangles = []
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if the contour has four vertices, add to rectangles
	if len(approx) == 4:
		rectangles += [approx]
		break


# Attempt to find second-largest rectangle to eliminate bold puzzle border
# doesn't matter if it isn't found, just makes image recognition better if it is
if rectangles == []:
	print("No puzzle found, try another image")
	sys.exit()

rectangles.sort(key=lambda x:cv2.contourArea(x),reverse=False)

if len(rectangles) == 1:
	rectangles = [None,rectangles[0]]

rawArea = rectangles[1].reshape(4,2)

# Work out which corners are what 
rawArea = rawArea[rawArea[:, 1].argsort()]
NW = min(rawArea[:2],key=lambda x: x[0])
SW = min(rawArea[-2:],key=lambda x: x[0])
NE = max(rawArea[:2],key=lambda x: x[0])
SE = max(rawArea[-2:],key=lambda x: x[0])

# puzzleFound = cv2.polylines(gray,np.array([NW,SW,NE,SE],np.int32).reshape((-1,1,2)),True,255,3)
# cv2.imshow("found",puzzleFound)

print(NW[0])
print(((SW[0]-NW[0])/8))
# Move corners to find numbers too
NW1 = [NW[0] + ((SW[0]-NW[0])/8),
	   NW[1] - ((SW[1]-NW[1])/8)]
NE1 = [NE[0] + ((SE[0]-NE[0])/8),
	   NE[1] - ((SE[1]-NE[1])/8)]

NE2 = [NE[0] + ((NE[0]-NW[0])/8),
	   NE[1] + ((NE[1]-NW[1])/8)]
SE1 = [SE[0] + ((SE[0]-SW[0])/8),
	   SE[1] + ((SE[1]-SW[1])/8)]

puzzleArea = np.array([NW, SW, NE, SE])
topArea = np.array([NW1,NE1,NE,NW])
sideArea = np.array([NE,NE2,SE,SE1])
puzzleFound = cv2.polylines(gray,np.array([NE,NE2,SE,SE1],np.int32).reshape((-1,1,2)),True,255,3)

# print (np.minimum(rawArea[2],rawArea[3]))

# extract the puzzle, apply a perspective transform to it
warped = four_point_transform(gray, puzzleArea)
topNum = four_point_transform(gray, topArea)
sideNum = four_point_transform(gray, sideArea)

# Get height and width
height,width = warped.shape
cellheight, cellwidth = height/8, width/8

cv2.imshow("gray",gray)
cv2.imshow("warped",warped)
cv2.imshow("topArea",topNum)
cv2.imshow("sideNum",sideNum)
cv2.waitKey(0) 