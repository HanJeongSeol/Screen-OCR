import time
import threading
from tkinter import *
from pororo import Pororo
import numpy as np
import cv2
from PIL import ImageGrab, Image
import socketio
import asyncio
import httpx
import queue
import pyautogui
global cnt
cnt = 0

class MyClient:
    def __init__(self,userIp):
        self.sio = socketio.Client()
        self.userIp = userIp
        self.headers = {'X-Forwarded-For': self.userIp}
        self.sio.connect('http://localhost:3306',self.headers)
        self.playlistId=None

        @self.sio.on('connect')
        def on_connect():
            print('서버 연결')
        
        @self.sio.on('check')
        def on_chek(data):
            print("서버로 전달한 데이터 확인 %s" % data)
        
        @self.sio.on('state')
        def on_state(data):
            print("소켓 연결 상태 : %s" %data)
        
        @self.sio.on('user')
        def on_state(data):
            print("연결된유저 : %s" %data)
            self.user = data

        @self.sio.on('playlist') 
        def on_state(data) :
            print("플레이리스트 아이디 : %s" % data)
            self.playlistId  = data

    def send_data(self,data):
        self.sio.emit('text', data)

    def disconnect(self):
        self.sio.disconnect()
    
    def send_clientId(self,data) : 
        self.sio.emit('clientIp',data)
        
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
            
    def stop(self) :
        self.__isRunning_ = False

    class WorkerThread(threading.Thread) :
        def __init__(self, threadTask) :
            threading.Thread.__init__(self)
            self.__threadTask_ = threadTask
            self.daemon = True

        def run(self) :
            try :
                self.__threadTask_.taskFunc()(self.__threadTask_.isRunning)
            except Exception as e : print(repr(e))
            self.__threadTask_.stop()

class CaptureGUI :
    def __init__(self,master,my_client=None) :
        self.master = master
        # self.my_client = my_client
        master.geometry("481x1174+1067+53")
        master.attributes('-alpha',0.8)
        master.attributes('-topmost',1)
        master.bind("<Configure>", self.setSize)
        self.width=None
        self.height=None
        self.root = master
        self.queue = queue.Queue()

        # self.user = user
        self.startButton = Button(self.master, text ="캡쳐시작", command=self.captureStart,anchor="center")
        self.startButton.pack(padx=5, pady=20)
        
        self.stopButton = Button(self.master, text ="정지", command=self.captureStop,anchor="center")
        self.stopButton.pack(padx=5, pady=20)

        self.captureTask = ThreadTask(self.capture)

    # def capture_specific_area(self):
    #     x, y, width, height = self.get_window_geometry()
    #     screenshot = pyautogui.screenshot(region=(x, y, width, height))
    #     screenshot.save("screenshot.png")

    def setSize(self,event):
        time.sleep(0.001)

        global coordinate 
        coordinate = list()


        width = self.root.winfo_width()
        height = self.root.winfo_height()

        coordinate.append(self.root.winfo_rootx())
        coordinate.append(self.root.winfo_rooty())
        coordinate.append(coordinate[0] + width)
        coordinate.append(coordinate[1]+height)
        
        self.coordinate = coordinate

        head = '캡쳐영역' + ' ' + str(width) + ' x ' + str(height) + ' ' + str(coordinate[0]) + ' x ' + str(coordinate[1])
        self.root.title(head)
        
        time.sleep(0.01)

    def show_frame(self, frame):
        if frame is not None:
            cv2.imshow('cat on chair', frame)
            cv2.waitKey(1)  # 1ms 기다리도록 수정하였습니다.

    def capture(self, isRunningFunc = None) :
        cap_coordinate = self.coordinate
        self.root.attributes('-alpha',0.8)
        self.root.geometry('100x300+100+100')
        self.root.update()
        global cnt
        poro_ocr = PororoOcr()
        # my_client = MyClient()
        # print("캡쳐안의 유저")
        # print(self.user)
        while True :
            startTime = time.time()
            try :
                if not isRunningFunc() :
                    # self.my_client.disconnect()
                    return
            except : pass
            pass
            cnt = cnt + 1
            time.sleep(1)

            # img = ImageGrab.grab(cap_coordinate)
            # frame = np.array(img)
            # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            # img = cv2.imread("talk1.png")
            # frame = self.highlight_specific_text_regions(img)
            # Contrast enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
            # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            # enhanced = clahe.apply(gray)
            
            # blurred = cv2.GaussianBlur(gray, (1, 1), 0)

            # Adaptive thresholding
            # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            #                             cv2.THRESH_BINARY_INV, 11, 1)
            
            # Dilation with a finer kernel
            # kernel = np.ones((1,1), np.uint8)

            # erode = cv2.dilate(thresh, kernel , iterations=1)
            # window = (self.width, self.height)
            # print(window)
            # img = img.resize(window, Image.Resampling.LANCZOS)
            # frame = np.array(img)
            # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # frame = cv2.bilateralFilter(frame, 9, 50, 50)

            # frame = cv2.GaussianBlur(frame, (5, 5), 0)
            # kernel_sharpen_3 =np.array([[-1, -1, -1],
            #                  [-1, 9, -1],
            #                  [-1, -1, -1]])

            # frame = cv2.filter2D(frame, -1, kernel_sharpen_3)
            # frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            #                    cv2.THRESH_BINARY_INV, 11, 1)
            # kernel = np.ones((3,3), np.uint8)
            # dilate = cv2.dilate(gray, kernel, iterations=1)


            # img_name = "image/talk%d_test.png" % cnt

            # cv2.imwrite(img_name,frame)
            text = poro_ocr.run_ocr("final.png")
            print(text)
            endTine = time.time()
            # self.my_client.send_data(text)

            print("소요시간 : " , endTine-startTime)

    def check_queue(self):
        try:
            frame = self.queue.get(0)
            self.show_frame(frame)
        except queue.Empty:
            pass

    def highlight_specific_text_regions(self,img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # # # Apply Gaussian blur to the image
        blurred = cv2.GaussianBlur(img, (5,5), 0)
        
        # # # Enhance sharpness using Unsharp Masking
        sharpened = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)

        return sharpened
    
    def captureStart(self) :
        # 캡쳐 시작 버튼을 누르는 시점의 width,heigt 저장
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        print("captureStart")
        self.captureTask.start()

    def captureStop(self) :
        print("captureStop")
        self.root.geometry("430x420+800+400")
        self.root.update()

        self.captureTask.stop()

    def preprocess_image_for_ocr(self,img: np.array) -> np.array:
        """
        Preprocessing for the input image for OCR with resizing and adaptive thresholding.
        
        Args:
        - img (np.array): The input image.
        
        Returns:
        - np.array: The preprocessed image.
        """

        # 1. Convert to Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Resize the image to enhance resolution to a higher factor
        resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

        # 3. Adaptive Thresholding for binarization
        binary = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv2.THRESH_BINARY_INV, 11, 2)
        
        return binary


def captureWidget(my_client=None):                # my_client 인자 추가
    root = Tk()
    capture_widget = CaptureGUI(root, my_client)  # my_client 전달
    root.mainloop()

# 소켓과 일차적으로 유저 정보를 받아오는 통신을 진행. 유저 정보 및 플리 저장시킬 그룹 선택 값을 서버에서 받아온다.
def userCheck(userIp):
    my_client = MyClient(userIp)
    while True:
        try:
            if my_client.playlistId is not None:
                my_client.send_clientId(my_client.userIp)
                return captureWidget(my_client)    # my_client 전달
        except:
            pass
# 공인 ip 가져오기
async def get_public_ip():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api64.ipify.org?format=json')
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            print(data)
            return data['ip']
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# ngrok URI에서 IP만 출력

def extract_ip_from_uri(uri):
    # 문자열을 "://" 기준으로 나누고 두 번째 요소를 선택합니다.
    # 이렇게 하면 "https://e02d-106-241-78-77.ngrok-free.app" 중에서 "e02d-106-241-78-77.ngrok-free.app" 부분이 선택됩니다.
    # 그리고 다시 "."으로 나누고 첫 번째 요소를 선택하면 "e02d-106-241-78-77"이 선택됩니다.
    # 그리고 "-"을 "."로 바꾸어서 "e02d.106.241.78.77"로 변환합니다.
    # 마지막으로 다시 "."으로 나누고 두 번째 요소를 선택하면 "106.241.78.77"이 선택됩니다.
    ip = uri.split("://")[1].split(".")[0].replace("-", ".").split(".",1)[1]
    return ip

async def main():
    captureWidget()
if __name__ == "__main__":
    asyncio.run(main())