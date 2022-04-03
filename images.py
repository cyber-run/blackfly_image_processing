import cv2
import PySpin
import EasyPySpin
import numpy as np
import os
import time
from tracker import *

start_time = time.time()

dir_path = 'D:\images\channel_10Hz'

background = cv2.imread("Resources/background.tif", cv2.IMREAD_GRAYSCALE)
background = background[240:840, 0:1440]

Files = os.listdir(dir_path)

kernel = None

# Create tracker object
tracker = EuclideanDistTracker()

y_disp = []
vel_list = []

for File in Files:
    # ----------- 1. Image processing -----------

    # Declare next image path in file
    img_path = os.path.join(dir_path, File)

    # Read image data from next image path
    original_image = cv2.imread(img_path)
    original_image = original_image[240:840, 0:1440]

    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Subtract background from image using preloaded background
    mask = cv2.subtract(background, image)

    # cv2.imshow("Images", image)     # show image after background subtraction

    # Apply binary threshold to image
    retval, mask = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)

    # Erode to remove smaller points from impurities in fluid
    # Dilate to increase size of particle mask
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=5)

    # ----------- 2. Object Detection -----------

    # Find contours in image mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    # Process contours for tracking
    for cnt in contours:
        cv2.drawContours(original_image, [cnt], -1, (0, 255, 0), 1)

        x, y, w, h = cv2.boundingRect(cnt)

        detections.append([x, y, w, h, 0])

    # ----------- 3. Object Tracking -----------
    box_ids = tracker.update(detections)

    for box_id in box_ids:
        x, y, w, h, id, vel = box_id
        vel = np.round(vel, 2)
        vel_list.append(vel)
        cv2.putText(original_image, str(id), (x, y - 25), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv2.putText(original_image, str(vel) + ' Micron/s', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        y_disp.append((y - image.shape[0]/2)*3.45)

    # Show mask
    # cv2.imshow("Mask", mask)
    # Show image
    cv2.imshow("Image", original_image)

    # if q is pressed end program, wait 2 seconds between processing images for real-time viewing
    key = cv2.waitKey(100)
    if key == 27:
        break
    if key == ord(' '):
        cv2.waitKey(-1)  # wait until any key is pressed

# destroy windows at end of program, should be automatic, but just for the case of memory issues
cv2.destroyAllWindows()

print(np.mean(y_disp))

# Converts list obj to NP array, so values less than 1, ie the initialising 0 values can easily be removed
vel_list = np.array(vel_list)
vel_list = vel_list[(vel_list > 5)]
print(np.mean(vel_list))

print("--- %s seconds ---" % (time.time() - start_time))
