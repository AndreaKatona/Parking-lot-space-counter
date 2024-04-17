'''
 ParkingSpacePicker.py loads an image showing parking spaces and allows users to add or delete parking spaces using mouse clicks.
 It draws the parking spaces on the image and stores them in a file for later use.
 The program runs until the user presses the "q" key to close the displayed image.
'''

import cv2
import pickle

# size of a parking spot
width, height = 107, 48

# try to load previously saved parking spaces
try:
    with open('CarParkPos', 'rb') as fin:
        posList = pickle.load(fin)
except:
    # if not found, start with empty list
    posList = []

# mouse click event handler


def mouseClick(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # add a new parking space on left click
        posList.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        # remove parking space on right click
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    # save the updated list
    with open('CarParkPos', 'wb') as fout:
        pickle.dump(posList, fout)


while True:
    img = cv2.imread('carParkImg.png')

    # draw the parking space on the image
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 0), 2)

    # display image
    cv2.imshow("image", img)

    # exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# close window
cv2.destroyAllWindows()
