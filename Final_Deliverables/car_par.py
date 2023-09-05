"""# **Import packages**"""

import cv2
import pickle
import cvzone
import numpy as np

"""# **Reading Input And Loading ROI File**"""

#vedio feed
cap = cv2.VideoCapture(r"C:\Users\PDP\flask\uploads\carParkingInput.mp4")
#Loading the ROI from parkingSlotPosition file
with open(r"C:\Users\PDP\flask\parkingSlotPosition", 'rb') as f:
   posList = pickle.load(f)
#Define width and height
width, height = 197, 48

"""# **Checking For Parking Space**"""

def checkParkingSpace(ImgPro):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        #Crop the image based on ROI
        imgCrop = ImgPro[y:y + height, x:x + width]

        # Counting the pixel values from cropped image
        count = cv2.countNonZero(imgCrop)
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spacecounter += 1
        else:
            color = (0, 0, 255) 
            thickness = 2
        #Draw the rectangle based on the condition defined above 
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    #Display the available  parking slot count / total parking slot count
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0,200,0))

"""# **Looping The Video**"""

if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
   cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

"""# **Frame Processing And Empty Parking Slot Counters**"""

while True:
    #Looping the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): 
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 

    #Reading frame by frame from video 
    Success, img = cap.read()
    #Converting to gray scale image
    img = cv2.imread(r"C:\Users\PDP\flask\uploads\carParkImg.png")
    cv2.imshow('original',img)
    cv2.waitKey(0)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur (imgGray, (3, 3), 1) # Applying blur to image
    # Applying threshold to the image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian= cv2.medianBlur (imgThreshold, 5) 
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    #Passing dilate image to the function
    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    cv2.waitKey(10)