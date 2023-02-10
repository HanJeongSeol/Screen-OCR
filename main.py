import numpy as np
import time
from PIL import ImageGrab
import cv2
from tkinter import *
def setSize(event):
    time.sleep(0.001)

    global coordinate 
    coordinate = list()


    width = root.winfo_width()
    height = root.winfo_height()

    coordinate.append(root.winfo_rootx())
    coordinate.append(root.winfo_rooty())
    coordinate.append(coordinate[0] + width)
    coordinate.append(coordinate[1]+height)

    head = '캡쳐영역' + ' ' + str(width) + ' x ' + str(height) + ' ' + str(coordinate[0]) + ' x ' + str(coordinate[1])
    root.title(head)

    time.sleep(0.01)

def capture(root, roi=[]) : 
    root.attributes('-alpha',0.0)
    root.update()
    img = ImageGrab.grab(roi)
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    localTime = time.localtime()
    nowTime = "%04d-%02d-%02d" % (localTime.tm_year, localTime.tm_mon, localTime.tm_mday)
    cv2.imwrite("image/talk_%s.png" % nowTime,frame)
    root.attributes('-alpha',0.8)
    return

def inputKey(event):
    if(event.char) == '1' : 
        capture(root,coordinate)

root = Tk()
root.title("캡처영역")
root.attributes('-alpha',0.8)
root.attributes('-topmost',1)
root.geometry("430x420+800+400")

root.bind("<Configure>" ,setSize)
root.bind("<Key>", inputKey)

setSize(None)

root.mainloop()
