import cv2
import EasyPySpin
import numpy as np


cap = EasyPySpin.VideoCapture(0)

while True:
    success, img = cap.read()

    small = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

    cv2.imshow("Video", small)

cap.release()
cv2.destroyAllWindows()
