import cv2
import EasyPySpin
import numpy as np


def main():
    cap = EasyPySpin.VideoCapture(0)

    print('--------Capturing frames--------')
    print('\nPress m to see the menu')
    thresh = 100
    in_delay = 100
    signal_length = 100

    while True:
        success, img = cap.read()

        if np.max(img) > thresh:
            # GPIO code

        if cv2.waitKey(1) & 0xFF == ord('m'):
            print('1. Set initial delay (ms)\n'
                  '2. Set signal length (ms)\n'
                  '3. Set threshold (0<x<255)\n'
                  '4. Quit\n')

            choice = int(input())

            if choice == 1:
                print("Enter initial delay(ms): ")
                in_delay = int(input())
            if choice == 2:
                print("Enter sigal length (ms): ")
                signal_length = int(input())
            if choice == 2:
                print("Enter sigal length (ms): ")
                signal_length = int(input())
            if choice == 4:
                break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
