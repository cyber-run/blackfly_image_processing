import cv2
import numpy as np
import os
import time
from tracker import *


start_time = time.time()

dir_path = 'D:\images\channel_10Hz'
files = os.listdir(dir_path)

background = cv2.imread("Resources/background.tif", cv2.IMREAD_GRAYSCALE)
background = background[245:780, 0:1440]

period = 1/10
scale = 1 / 535
kernel = None

# Create tracker object
tracker = EuclideanDistTracker(period, scale)
radial_d_list = []
vel_list = []

for file in files:
    # ------------------------------------------- 1. Image processing -------------------------------------------
    # Declare next image path in file
    img_path = os.path.join(dir_path, file)

    # Read image data from next image path
    original_image = cv2.imread(img_path)
    original_image = original_image[245:780, 0:1440]

    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Subtract background from image using preloaded background
    mask = cv2.subtract(background, image)

    # Apply binary threshold to image
    retval, mask = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)

    # Erode and dilate to improve mask accuracy
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=5)

    # -------------------------------------------- 2. Object Detection --------------------------------------------
    # Find contours in image mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    # Process contours for tracking
    for cnt in contours:
        if 100 < cv2.contourArea(cnt) < 300:
            cv2.drawContours(original_image, [cnt], -1, (0, 255, 0), 1)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h, 0])

    # -------------------------------------------- 3. Object Tracking --------------------------------------------
    box_ids = tracker.update(detections)

    for box_id in box_ids:
        x, y, w, h, id, vel = box_id

        vel = np.round(vel, 2)
        radial_disp = np.round((y - image.shape[0] / 2) * scale, 2)

        if vel > 0.5:
            vel_list.append(vel)
            radial_d_list.append(radial_disp)

        cv2.putText(original_image, 'ID: ' + str(id), (x, y - 35), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv2.putText(original_image, str(vel) + ' mm/s', (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv2.putText(original_image, str(radial_disp) + ' mm', (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    # Show image
    cv2.imshow("Image", original_image)

    # 'q' key to terminate, space bar to pause
    key = cv2.waitKey(10)
    if key == 27:
        break
    if key == ord(' '):
        cv2.waitKey(-1)

# destroy windows at end of program, should be automatic, but just for the case of memory issues
cv2.destroyAllWindows()

# Converts list obj to NP array, so values less than 1, ie the initialising 0 values can easily be removed
vel_list = np.array(vel_list)
radial_d_list = np.array(radial_d_list)

print(np.mean(vel_list))
print(np.mean(radial_d_list))

np.save('velocity', vel_list)
np.save('radial_displacement', radial_d_list)

print("--- %s seconds ---" % (time.time() - start_time))
