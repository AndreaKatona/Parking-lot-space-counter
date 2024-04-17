'''
main.py implements a parking space management system using OpenCV.
The script counts the number of free parking spaces and displays this information on the video feed.
The script runs continuously until the user interrupts it.
'''

import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as fin:
    posList = pickle.load(fin)

width, height = 107, 48


def checkParkingSpace(imgProcess):

    spaceCounter = 0
    for pos in posList:
        x, y = pos

        # crop the parking space from the processed image
        imgCrop = imgProcess[y:y+height, x:x+width]

        # count non-zero pixels (occupied space) in the cropped image
        count = cv2.countNonZero(imgCrop)

        # cvzone.putTextRect(imgCrop, str(count), (x, y+height-5),scale=1, thickness=1, offset=0)
        
        if count < 900:
            color = (0, 255, 0)
            spaceCounter += 1
        else:
            color = (0, 0, 255)

        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, 2)

    cvzone.putTextRect(img, f'Free: {str(spaceCounter)}/{len(posList)}', (100, 50),
                       scale=3, thickness=5, offset=20, colorR=(0, 200, 0))


while True:

    # reset video capture to beginning if end of video is reached
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # read frame from video
    success, img = cap.read()

    # convert image from RGB to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # reduce noise and smooth out image
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # calculate the threshold for each pixel based on the local neighborhood
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    # applie median filtering to the thresholded image
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    # create a 3x3 kernel with all elements set to 1
    kernel = np.ones((3, 3), np.int8)

    # dilation is applied to the median-filtered image
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # check parking spaces and draw rectangles on image
    checkParkingSpace(imgDilate)

    cv2.imshow("Image", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# close window
cv2.destroyAllWindows()
