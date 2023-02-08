import numpy as np
import time
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

root = Tk()
root.title("캡처영역")
root.attributes('-alpha',0.8)
root.attributes('-topmost',1)
root.geometry("430x420+800+400")

root.bind("<Configure>" ,setSize)
setSize(None)

root.mainloop()