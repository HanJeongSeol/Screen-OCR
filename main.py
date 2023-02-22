import time
import threading
import keyboard
import config.util as Util
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
    

class Capture(PororoOcr) :
    def getFileName():
        localTime = time.localtime()
        nowTime = "%04d-%02d-%02d" % (localTime.tm_year, localTime.tm_mon, localTime.tm_mday)
        return nowTime

            
    def capture(root, roi=[]) : 
        po = PororoOcr()
        global cnt
        root.attributes('-alpha',0.0)
        root.update()
        while True :
            startPoint = time.time()
            cnt = cnt+1
            img = ImageGrab.grab(roi)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_name = "image/talk_%s_%d.png" % (Capture.getFileName(),cnt)
            cv2.imwrite(img_name,frame)
            text = po.run_ocr(img_path=img_name)
            print(text)
            endPoint=time.time()
            print("시간 : " , endPoint - startPoint)
            key = cv2.waitKey(1)
            if keyboard.is_pressed(Util.KEY_STOP):
                root.attributes('-alpha', 0.8)
                break
        
        return

    def destroy(root) :
        root.destroy()
        return

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
        threading.Thread(target=Capture.capture(root,coordinate), daemon=True).start()

    if keyboard.is_pressed(Util.WIDGET_DESTROY):
        threading.Thread(target=Capture.destroy(root), daemon=True).start()



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



# 비동기처리로 캡쳐한 사진의 텍스트 추출이 완료되어야만 다음 작업 수행하도록 변경
# 다음 작업 -> 어떻게 모듈화할지, 현재 클래스로 나뉘어져있고
# 모듈화를 수행했을 때 비동기 작업 처리 형식 고민
