import cv2
import numpy as np

def validFrame(rgbImage, template):
    grayFrame = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)

    # Match template image to frame
    result = cv2.matchTemplate(grayFrame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        return True
    return False

def compareFrames(toCompare, standardImg):
    # Convert to HSV
    standardHSV = cv2.cvtColor(standardImg, cv2.COLOR_BGR2HSV)
    compHSV = cv2.cvtColor(toCompare, cv2.COLOR_BGR2HSV)

    # Generate histograms and normalize
    standardHist = cv2.calcHist([standardHSV], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(standardHist, standardHist).flatten()
    compHist = cv2.calcHist([compHSV], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(compHist, compHist).flatten()

    # Return metric val
    return cv2.compareHist(standardHist, compHist, cv2.HISTCMP_CHISQR)

def convertToJPG(frame):
    return cv2.imdecode(cv2.imencode('.jpg', frame)[1], cv2.IMREAD_UNCHANGED)