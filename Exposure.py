import cv2
import EasyPySpin
import numpy as np

cap = EasyPySpin.VideoCapture(0)

exp = 1

while exp !== 0:
    print("Enter frame exposure (ms): ")
    exp = int(input())
    cap.set_pyspin_value("ExposureAuto", 'Off')
    cap.set_pyspin_value("ExposureTime", exp*1000)

cap.release()
