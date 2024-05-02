from TelloLib.Control import Control
from Detection.distance import measure
import Detection.ann_detect as an
from TelloLib.Video import VideoGet, VideoShow
from TelloLib.counter import CountsPerSec
import cv2 as cv
import numpy as np
import keyboard as kb



#function to put iteration speed on the shown image
def putIPS(frame, ips):
    cv.putText(frame, "{:.0f} iteration/sec".format(ips), (10, 450), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

#main function to control the drone's movement based on its vision
def main():
    dist = 999
    x_mid = 320
    y_mid = 240
    dim = (640, 480)
    a = 0
    b = 0
    c = 0
    d = 0
    udp = 'udp://@0.0.0.0:11111'
    model = an.loadModel()

    control = Control()

    control.send_command('command')
    control.send_command('streamon')

    vid = VideoGet(udp).start()
    scr = VideoShow(vid.frame).start()
    cps = CountsPerSec().start()

    control.take_off()
    #control.descend(20)
    while True:
        img = vid.frame
        #if count == 0:
        img = cv.resize(img, dim)
        coord, label, img = an.detect(img, model)
        if coord:
            coord = coord[0]
            label = label[0]
            b = 5
            #x_mid = x_mid - (coord[2] / 2)
            dist = measure(coord, label)
            img = cv.putText(img, f'Distance {dist} cm', (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 0), 1, cv.LINE_AA)
            if coord[0] < x_mid:
                a = -5
            elif coord[0] > x_mid: 
                a = 5
            else:
                a = 0
        else:
            b = 0
            a = 0
        if dist <= 100.0:
            break
        #cv.imshow("Flight", img)
        print("IPS: %.2f"%(cps.countsPerSec()))
        scr.frame = img 
        if kb.is_pressed("a"):
            vid.stop()
            scr.stop()
            break
        control.rc_mode(a, b, c, d)
        
    control.rc_mode(0, 0, 0, 0)
    control.land()

if __name__ == "__main__":
    main()
