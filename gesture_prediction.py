from PIL import Image
import imutils
import numpy as np
from keras.models import load_model
import cv2
import urllib
import http

# Load Saved Model
model = load_model('my_model6.h5')
root_url = "http://192.168.43.11"  # O ESP's url, ex: https://192.168.102 (Esp serial prints it when connected to wifi)


def sendRequest(s,lms,rms):
    try:
        url = root_url + '/' + s + '/' + str(lms) + '/' + str(rms)
        n = urllib.request.urlopen(url).read()  # send request to ESP
        n = n.decode("utf-8")
        return n
    except http.client.HTTPException as e:
        return e





camera = cv2.VideoCapture(0)
top, right, bottom, left = 80, 360, 280, 560
cv2.namedWindow("TrackedBars")
cv2.resizeWindow("TrackedBars", 640, 240)

start_recording=False

def on_trackbar(val):
    hue_min = cv2.getTrackbarPos("Hue Min", "TrackedBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackedBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackedBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackedBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackedBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackedBars")
    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])

    imgMASK = cv2.inRange(imgHSV, lower, upper)
    r,c=imgMASK.shape

    kernelOpen = np.ones((5, 5))  # if jiggers are present other than yellow area
    kernelClose = np.ones((2, 2))

    # apply morphology to avoid jiggers
    maskOpen = cv2.morphologyEx(imgMASK, cv2.MORPH_OPEN, kernelOpen)
    maskOpen = cv2.resize(maskOpen, (r, c))
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    maskClose = cv2.resize(maskClose, (r, c))
    cv2.imshow("mo", maskOpen)
    cv2.imshow("mc", maskClose)
    return maskClose



cv2.createTrackbar("Hue Min", "TrackedBars", 25, 179, on_trackbar)
cv2.createTrackbar("Hue Max", "TrackedBars", 179, 179, on_trackbar)
cv2.createTrackbar("Sat Min", "TrackedBars", 65, 255, on_trackbar)
cv2.createTrackbar("Sat Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("Val Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Val Max", "TrackedBars", 255, 255, on_trackbar)


def getPredictedClass(gray_image):
    X = np.array(gray_image)
    # X=loadedImages
    X = X.reshape(1,X.shape[0], X.shape[1], 1)
    X = X.astype('float32')
    X /= 255
    prediction = model.predict(X)
    return np.argmax(prediction)

# pp
prev_predict_class=0
move_class=['Maintain Previous State', 'Move Left', 'Move Right','Move Backward','Move Forward','STOP']
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
        test_img=on_trackbar(0)
        # Wait until user press some key
        cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)
        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)
        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

        if keypress == ord("s"):
            start_recording = True
        if(start_recording):
            predictedClass=getPredictedClass(test_img)
            print(move_class[predictedClass])
            if(predictedClass==0 or prev_predict_class==predictedClass):
                pass
            elif (predictedClass == 1):
                sendRequest('l',400,400)
            elif (predictedClass == 2):
                sendRequest('r',400,400)
            elif (predictedClass == 3):
                sendRequest('b',400,400)
            elif (predictedClass == 4):
                sendRequest('f',400,400)
            elif (predictedClass == 5):
                sendRequest('s',0,0)
            prev_predict_class=predictedClass
    else:
        break

camera.release()
cv2.destroyAllWindows()
# 0-blank---- continue
# 1-one----left
# 2-two--- right
# 3-fist----backward
# 4-four----forward
# 5-five ----stop