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

        imgCrop = imgProcess[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        #cvzone.putTextRect(img, str(count), (x, y+height-5),
        #                   scale=1, thickness=1, offset=0)

        if count < 900:
            color = (0, 255, 0)
            spaceCounter += 1 
        else:
            color = (0, 0, 255)

        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, 2)
        
    cvzone.putTextRect(img, f'Free: {str(spaceCounter)}/{len(posList)}', (100, 50),
                           scale=3, thickness=5, offset=20, colorR=(0,200,0))

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.int8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("Image", img)
    # cv2.imshow("ImageGray", imgMedian)
    cv2.waitKey(10)
