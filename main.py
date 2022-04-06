import cv2
import EasyPySpin
import numpy as np


def main():
    cap = EasyPySpin.VideoCapture(0)

    # Grab some camera variables
    temp = cap.get_pyspin_value("DeviceTemperature")

    count = 0

    print(temp)

    # _, img = cap.read()
    # green_img = np.zeros(img.shape)

    print('--------Capturing frames--------')
    print('\nPress m to see the menu')

    while True:
        success, img = cap.read()

        cv2.imshow("Video", img)
        # green_channel = img[:, :, 1]
        # green_img[:, :, 1] = green_channel
        # cv2.imshow("Green Channel", green_img)

        if cv2.waitKey(1) & 0xFF == ord('m'):
            print('1. Set height\n'
                  '2. Set width\n'
                  '3. Set exposure\n'
                  '4. Set fps\n'
                  '5. Save image\n'
                  '6. Quit')

            choice = int(input())

            if choice == 1:
                print("Enter frame height: ")
                height = int(input())
                cap.set_pyspin_value("Height", height)
            if choice == 2:
                print("Enter frame width: ")
                width = int(input())
                cap.set_pyspin_value("Width", width)
            if choice == 3:
                print("Enter frame exposure: ")
                exp = int(input())
                cap.set_pyspin_value("ExposureAuto", 'Off')
                cap.set_pyspin_value("ExposureTime", exp)
            if choice == 4:
                print("Enter FPS: ")
                fps = int(input())
                cap.set_pyspin_value("AcquisitionFrameRateEnable", True)
                cap.set_pyspin_value("AcquisitionFrameRate", fps)
            if choice == 5:
                cv2.imwrite("frame%d.png" % count, img)  # save frame as JPEG file
                print('Successfully saved: ' + str(count))
                count += 1
            if choice == 6:
                break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
