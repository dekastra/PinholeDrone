from threading import Thread
import cv2

class VideoGet:
    def __init__(self, src='udp://@0.0.0.0:11111'):
        self.stream = cv2.VideoCapture(src)
        if not self.stream.isOpened():
            self.stream.open(src)
        (self.ret, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            '''if not self.ret:
                print("trap #2")
                self.stop()
            else:
                (self.ret, self.frame) = self.stream.read()'''
            (self.ret, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
        #self.stream.release()

class VideoShow:
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            if self.frame is not None:
                cv2.imshow("Flight", self.frame)
            if cv2.waitKey(1) == ord('q'):
                self.stopped = True

    def stop(self):
        self.stopped = True
