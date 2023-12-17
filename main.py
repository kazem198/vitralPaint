import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# 3
colorPaint = (255, 0, 0)
px = 0
py = 0
imgBackground = np.ones((720, 1280, 3), np.uint8)*255
############################################################

imgHeaders = []
headers = os.listdir("headers")
print(headers)
for header in headers:
    img = cv2.imread(f'headers/{header}')
    imgHeaders.append(img)

detector = HandDetector(detectionCon=0.8)

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    img[0:150, :] = imgHeaders[0]

    hands, img = detector.findHands(img, draw=True, flipType=True)
    if hands:

        hand1 = hands[0]
        lmList = hand1["lmList"]

        finger = detector.fingersUp(hand1)

        # print(lmList[8])

        if finger[1] and finger[2]:
            x1, y1 = lmList[8][0:2]
            x2, y2 = lmList[12][0:2]

            cv2.rectangle(img, (x1, y1),
                          (x2, y2), colorPaint, cv2.FILLED)

            centerX = int((x2+x1) / 2)
            centerY = int((y2+y1)/2)
            if centerY < 150:
                if 300 < centerX < 500:
                    colorPaint = (255, 0, 0)

                elif 500 < centerX < 700:
                    colorPaint = (0, 0, 255)

                elif 700 < centerX < 900:
                    colorPaint = (0, 255, 0)

                elif 1100 < centerX < 1300:
                    colorPaint = (255, 255, 255)

        #
        #     cv2.circle(img, (centerX, centerY), 5, (0, 0, 0), cv2.FILLED)

        #     print("section")

        elif finger[1] and lmList[8][1] > 150:
            x, y = lmList[8][0:2]

            if px == 0 and py == 0:
                px = x
                py = y

            cv2.circle(img, (x, y), 30, colorPaint, cv2.FILLED)
            if colorPaint == (255, 255, 255):
                cv2.line(img, (x, y), (px, py), colorPaint, 70)
                cv2.line(imgBackground, (x, y), (px, py), colorPaint, 70)
            else:
                cv2.line(img, (x, y), (px, py), colorPaint, 20)
                cv2.line(imgBackground, (x, y), (px, py), colorPaint, 20)
            px = x
            py = y

        #     print("draw")


#     add = cv2.addWeighted(img, .5, imgBackground, .5, 0)
    add = cv2.bitwise_and(img, imgBackground)
    cv2.imshow("img", img)
    cv2.imshow("imgBackground", imgBackground)
    cv2.imshow("add", add)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
