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

def captureWidget():
    class CaptureGUI :
        def __init__(self,master) :
            self.master = master
            master.geometry("430x420+800+400")
            master.attributes('-alpha',0.8)
            master.attributes('-topmost',1)
            master.bind("<Configure>", self.setSize)

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

