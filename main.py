import time
import threading
from tkinter import *
import tkinter.font
from pororo import Pororo
import numpy as np
import cv2
from PIL import ImageGrab


global cnt
cnt = 0

class PororoOcr:
    def __init__(self, model: str = "brainocr", lang: str = "ko", **kwargs):
        self.model = model
        self.lang = lang
        self._ocr = Pororo(task="ocr", lang=lang, model=model, **kwargs)
        self.img_path = None
        self.ocr_result = {}

    def run_ocr(self, img_path: str, debug: bool = False):
        self.img_path = img_path
        self.ocr_result = self._ocr(img_path, detail=True)

        if self.ocr_result['description']:
            ocr_text = self.ocr_result["description"]
        else:
            ocr_text = "No text detected."

        if debug:
            self.show_img_with_ocr()

        return ocr_text

class ThreadTask() :
    def __init__(self, taskFunc) :
        self.__taskFunc_ = taskFunc
        self.__workerThread_ = None
        self.__isRunning_ = False

    def taskFunc(self) :
        return self.__taskFunc_

    def isRunning(self) :
        return self.__isRunning_ and self.__workerThread_.is_alive()
    
    def start(self) :
        if not self.__isRunning_ :
            self.__isRunning_ = True
            self.__workerThread_ = self.WorkerThread(self)
            self.__workerThread_.start()

    class WorkerThread(threading.Thread) :
        def __init__(self, threadTask) :
            threading.Thread.__init__(self)
            self.__threadTask_ = threadTask

        def run(self) :
            try :
                self.__threadTask_.taskFunc()(self.__threadTask_.isRunning)
            except Exception as e : print(repr(e))
            self.__threadTask_.stop()

def captureWidget():
    class CaptureGUI :
        def __init__(self,master) :
            self.master = master
            master.geometry("430x420+800+400")
            master.attributes('-alpha',0.8)
            master.attributes('-topmost',1)
            master.bind("<Configure>", self.setSize)

            self.startButton = Button(self.master, text ="캡쳐시작")
            self.startButton.pack(padx=5, pady=20)
            
            self.stopButton = Button(self.master, text ="정지")
            self.stopButton.pack(padx=5, pady=20)

        def setSize(self,event):
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
    captureWidget = CaptureGUI(root)
    root.mainloop()

if __name__ == "__main__" :
    captureWidget()

