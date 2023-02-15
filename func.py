import time
import numpy as np
import cv2
import keyboard
from PIL import ImageGrab
import config.util as Util

global cnt
cnt = 0

def getFileName():
    localTime = time.localtime()
    nowTime = "%04d-%02d-%02d" % (localTime.tm_year, localTime.tm_mon, localTime.tm_mday)
    return nowTime

        
def capture(root, roi=[]) : 
    global cnt
    print(roi)
    root.attributes('-alpha',0.0)
    root.update()
    startPoint = time.time()
    while True :
        cnt = cnt+1
        img = ImageGrab.grab(roi)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if(cnt%21 ==0) :
            cv2.imwrite("image/talk_%s_%d.png" % (getFileName(),cnt) ,frame)
            print(cnt)
        key = cv2.waitKey(1)
        if keyboard.is_pressed(Util.KEY_STOP):
            root.attributes('-alpha', 0.8)
            break

    endPoint=time.time()
    print("시간 : " , endPoint - startPoint)
    return

def destroy(root) :
    root.destroy()
    return