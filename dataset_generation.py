# import cv2
# import numpy as np
# from sklearn.metrics import pairwise
#
# cap = cv2.VideoCapture(0)
# kernelOpen = np.ones((5, 5))  # if jiggers are present other than yellow area
# kernelClose = np.ones((20, 20))  # if jiggers are present in yellow area
#
# # HSV color range which should be detected
# lb = np.array([20, 100, 100])
# ub = np.array([120, 255, 255])
#
# while True:
#     ret, frame = cap.read()
#     flipped = cv2.flip(frame, 1)
#     flipped = cv2.resize(flipped, (500, 400))
#
#     # use HSV of yellow to detect only yellow color
#     imgSeg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     imgSegFlipped = cv2.flip(imgSeg, 1)
#     imgSegFlipped = cv2.resize(imgSegFlipped, (500, 400))
#
#     # masking and filtering all shades of yellow
#     mask = cv2.inRange(imgSegFlipped, lb, ub)
#     mask = cv2.resize(mask, (500, 400))
#
#     # apply morphology to avoid jiggers
#     maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
#     maskOpen = cv2.resize(maskOpen, (500, 400))
#     maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
#     maskClose = cv2.resize(maskClose, (500, 400))
#
#     final = maskClose
#     conts, h = cv2.findContours(maskClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#
#     if (len(conts) != 0):  # draws the contours of that object which has the highest
#         b = max(conts, key=cv2.contourArea)
#         west = tuple(b[b[:, :, 0].argmin()][0])  # gives the co-ordinate of the left extreme of contour
#         east = tuple(b[b[:, :, 0].argmax()][0])  # above for east i.e right
#         north = tuple(b[b[:, :, 1].argmin()][0])
#         south = tuple(b[b[:, :, 1].argmax()][0])
#         centre_x = (west[0] + east[0]) / 2
#         centre_y = (north[0] + south[0]) / 2
#
#         cv2.drawContours(flipped, b, -1, (0, 255, 0), 3)
#         cv2.circle(flipped, west, 6, (0, 0, 255), -1)
#         cv2.circle(flipped, east, 6, (0, 0, 255), -1)
#         cv2.circle(flipped, north, 6, (0, 0, 255), -1)
#         cv2.circle(flipped, south, 6, (0, 0, 255), -1)
#         cv2.circle(flipped, (int(centre_x), int(centre_y)), 6, (255, 0, 0), -1)  # plots centre of the area
#
#     cv2.imshow('video', flipped)
#     # cv2.imshow('mask', mask)
#     # cv2.imshow('mask open', maskOpen)
#     # cv2.imshow('mask close', maskClose)
#     if cv2.waitKey(1) & 0xFF == ord(' '):  # exiting
#         break
#
# cap.release()
# cv2.destroyAllWindows()
import cv2
import numpy as np
import imutils

def empty(i):
    pass

path = "temp.png"
camera = cv2.VideoCapture(0)
top, right, bottom, left = 80, 360, 280, 560
cv2.namedWindow("TrackedBars")
cv2.resizeWindow("TrackedBars", 640, 240)

start_recording=False
image_num=0



def on_trackbar(val,image_num):
    hue_min = cv2.getTrackbarPos("Hue Min", "TrackedBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackedBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackedBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackedBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackedBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackedBars")
    # lower=[22,67,0]
    # upper=[179,255,255]
    # lower=np.array(lower)
    # upper=np.array(upper)
    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])

    imgMASK = cv2.inRange(imgHSV, lower, upper)
    r,c=imgMASK.shape

    kernelOpen = np.ones((5, 5))  # if jiggers are present other than yellow area
    kernelClose = np.ones((4, 4))

    # apply morphology to avoid jiggers
    maskOpen = cv2.morphologyEx(imgMASK, cv2.MORPH_OPEN, kernelOpen)
    maskOpen = cv2.resize(maskOpen, (r, c))
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    maskClose = cv2.resize(maskClose, (r, c))


    # cv2.imshow("Output1", img)
    # cv2.imshow("Output2", imgHSV)
    # cv2.imshow("Mask", imgMASK)
    cv2.imshow("mo", maskOpen)
    cv2.imshow("mc", maskClose)
    if start_recording:
        # Mention the directory in which you wanna store the images followed by the image name
        cv2.imwrite("C:/Users/DELL/PycharmProjects/btech_p/Dataset/7/" + str(image_num) + '.png', maskClose)
        print("imgnum", image_num)
        image_num += 1
    return image_num



cv2.createTrackbar("Hue Min", "TrackedBars", 0, 179, on_trackbar)
cv2.createTrackbar("Hue Max", "TrackedBars", 179, 179, on_trackbar)
cv2.createTrackbar("Sat Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Sat Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("Val Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Val Max", "TrackedBars", 255, 255, on_trackbar)



while(True):
    (grabbed, frame) = camera.read()
    if (grabbed == True):
        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        clone = frame.copy()
        (height, width) = frame.shape[:2]
        roi = frame[top:bottom, right:left]

        imgHSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # Show some stuff
        image_num=on_trackbar(0,image_num)
        # Wait until user press some key
        cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)
        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)
        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q") or image_num > 100:
            break

        if keypress == ord("s"):
            start_recording = True
    else:
        break

camera.release()
cv2.destroyAllWindows()

# [22,67,0]
# [179,255,255]