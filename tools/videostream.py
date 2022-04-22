from threading import Thread
import cv2

class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.ret, self.frame) = self.stream.read()
        self.stopped = False
        self.validFrameFound = False
        self.validFrame = self.frame

    def start(self):
        # Start video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Loop indefinitely
        while True:
            # Stop if indicator set to true
            if self.stopped: return
            # Get next frame
            (self.ret, self.frame) = self.stream.read()

    def read(self):
        # Return the current frame
        return self.frame
    
    def foundValidFrame(self, image):
        # Signal that a valid frame has been found and save it to be used later
        self.validFrameFound = True
        self.validFrame = image
    
    def resetValidFrame(self):
        # Reset the valid frame signifier
        self.validFrameFound = False

    def stop(self):
        # Stop the thread and release any resources
        self.stopped = True