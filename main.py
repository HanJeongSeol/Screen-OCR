import time
import threading
import func as Func
import keyboard
import util as Util
from tkinter import *
import tkinter.font



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


def inputKey(event):
    global coordinate
    
    if keyboard.is_pressed(Util.KEY_START): 
        threading.Thread(target=Func.capture(root,coordinate), daemon=True).start()

    if keyboard.is_pressed(Util.WIDGET_DESTROY):
        threading.Thread(target=Func.destroy(root), daemon=True).start()

root = Tk()
root.title("캡처영역")
root.attributes('-alpha',0.8)
root.attributes('-topmost',1)
root.geometry("430x420+800+400")


root.bind("<Configure>" ,setSize)
root.bind("<Key>", inputKey)

font=tkinter.font.Font(size=20, weight ='bold', underline=True)
Msg = Label(root, text="1. 캡쳐시작 : %s" % Util.KEY_START, font=font)
Msg.pack(padx = 5, pady = 20)
Msg = Label(root, text="2. 캡쳐종료 : %s" % Util.KEY_STOP,  font=font)
Msg.pack(padx = 5, pady = 20)
Msg = Label(root, text="3. 프로그램 종료 : %s" % Util.WIDGET_DESTROY, font=font)
Msg.pack(padx = 5, pady = 20)

setSize(None)

root.mainloop()


