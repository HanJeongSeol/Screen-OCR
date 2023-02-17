import time
import numpy as np
import cv2
import keyboard
from PIL import ImageGrab
import config.util as Util
from pororo import Pororo

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
    