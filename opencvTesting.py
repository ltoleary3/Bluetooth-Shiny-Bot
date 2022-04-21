import matplotlib.pyplot as plt
import numpy as np
import cv2

def validFrame(rgbImage, template):
    grayFrame = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)

    # Match template image to frame
    result = cv2.matchTemplate(grayFrame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        return True
    return False

def compareFrames(toCompare):
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

if __name__ == "__main__":
    pokemon = 'regice'
    template = cv2.imread('assets/{0}/{0}Appeared.jpg'.format(pokemon), 0)
    standardImg = cv2.imread('assets/{0}/{0}Standard.jpg'.format(pokemon))
    print('temp: {}'.format(template.shape))
    print('base: {}'.format(standardImg.shape))
    vidCap = cv2.VideoCapture('regice.mp4')
    if not vidCap.isOpened(): exit()
    toCompare = None
    print('w: {0}\nh: {1}'.format(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH), vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    while True:
        success,frame = vidCap.read()
        if not success: break
        if validFrame(frame, template):
            toCompare = cv2.imdecode(cv2.imencode('.jpg', frame)[1], cv2.IMREAD_UNCHANGED)

    if (toCompare is not None):
        print('Found live image, comparing to standard')
        val = compareFrames(toCompare)
    
    if val >= 0.25:
        print('Shiny?!')
    else:
        print('Restarting...')
