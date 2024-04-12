import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as fin:
    posList = pickle.load(fin)

width, height = 107, 48


def checkParkingSpace():
    for pos in posList:
        x, y = pos
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 0), 2)
        
        imgCrop = img[y:y+height, x:x+width]
        cv2.imshow(str(x*y), imgCrop)


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    checkParkingSpace()

    cv2.imshow("Image", img)
    cv2.waitKey(10)
