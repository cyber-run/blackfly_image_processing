import cv2
import PySpin
import EasyPySpin
import numpy as np


def main():
    cap = EasyPySpin.VideoCapture(0)

    height = 400
    width = 400

    # Set camera variables
    cap.set_pyspin_value("Width", width)
    cap.set_pyspin_value("Height", height)

    cap.set_pyspin_value("AcquisitionFrameRateEnable", True)
    cap.set_pyspin_value("AcquisitionFrameRate", 5.0)

    # Grab some camera variables
    temp = cap.get_pyspin_value("DeviceTemperature")
    fps = cap.get_pyspin_value("AcquisitionResultingFrameRate")

    print(temp, fps)

    while True:
        success, img = cap.read()

        cv2.imshow("Video", img)

        img_canny = cv2.Canny(img,100,100)

        cv2.imshow("Canny Video", img_canny)

        print(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == "__main__":
    main()
