from TelloLib.Control import Control
from Detection.distance import measure
import Detection.ann_detect as an
import cv2 as cv
import numpy as np
import keyboard as kb

model = an.loadModel()
udp = 'udp://@0.0.0.0:11111'

control = Control()

control.send_command('command')
control.send_command('streamon')

vid = cv.VideoCapture(udp)
if not vid.isOpened():
    vid.open(udp)
ret = False
count = 0
while True:
    ret, img = vid.read()
    print("count", count)
    if ret and count == 0:
        img = cv.resize(img, (640, 480))
        coord, label, img = an.detect(img, model)
        if coord:
            coord = coord[0]
            label = label[0]
            dist = measure(coord, label)
            img = cv.putText(img, f'Distance {dist} cm', (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 0), 1, cv.LINE_AA)
        cv.imshow("Flight", img)
    count = (count + 1) % 8
        
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    

vid.release()
cv.destroyAllWindows()
control.send_command('streamoff')


