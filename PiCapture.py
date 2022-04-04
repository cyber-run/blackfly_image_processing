import cv2
import EasyPySpin

cap = EasyPySpin.VideoCapture(0)

# Get width/height/fps from user
print("Enter frame width: ")
width = int(input())
print("Enter frame height: ")
height = int(input())
print("Enter FPS: ")
fps = int(input())
print('Enter number of photos to take: ')
num = int(input())

# Set camera variables
cap.set_pyspin_value("Width", width)
cap.set_pyspin_value("Height", height)

cap.set_pyspin_value("AcquisitionFrameRateEnable", True)
cap.set_pyspin_value("AcquisitionFrameRate", fps)

# Grab FPS for check
fps = cap.get_pyspin_value("AcquisitionResultingFrameRate")

print('--------Capturing at frame rate: ' + str(fps) + '--------')

count = 0

success = True
while count < num + 1:
    success, image = cap.read()
    cv2.imwrite("frame%d.png" % count, image)  # save frame as JPEG file
    print('Successfully saved: ' + str(count))
    count += 1

cap.release()
