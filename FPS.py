import cv2
import EasyPySpin
import numpy as np

cap = EasyPySpin.VideoCapture(0)

fps = 1

while fps !== 0:
    print("Enter FPS: ")
    fps = int(input())
    cap.set_pyspin_value("AcquisitionFrameRateEnable", True)
    cap.set_pyspin_value("AcquisitionFrameRate", fps)

cap.release()
