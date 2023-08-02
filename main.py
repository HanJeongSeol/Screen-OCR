import time
import threading
from tkinter import *
from pororo import Pororo
import numpy as np
import cv2
from PIL import ImageGrab
import socketio
import webbrowser
import asyncio
import httpx


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
    def __init__(self,master,my_client) :
        self.master = master
        self.my_client = my_client
        master.geometry("430x420+800+400")
        master.attributes('-alpha',0.8)
        master.attributes('-topmost',1)
        master.bind("<Configure>", self.setSize)
        self.root = master
        # self.user = user
        self.startButton = Button(self.master, text ="캡쳐시작", command=self.captureStart,anchor="center")
        self.startButton.pack(padx=5, pady=20)
        
        self.stopButton = Button(self.master, text ="정지", command=self.captureStop,anchor="center")
        self.stopButton.pack(padx=5, pady=20)

        self.captureTask = ThreadTask(self.capture)

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
                    self.my_client.disconnect()
                    return
            except : pass
            pass
            cnt = cnt + 1
            time.sleep(1)
            img = ImageGrab.grab(cap_coordinate)
            frame = np.array(img)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img_name = "image/talk%d_test.png" % cnt
            cv2.imwrite(img_name,frame)
            text = poro_ocr.run_ocr(img_path=img_name)
            self.my_client.send_data(text)
            endTine = time.time()
            print("소요시간 : " , endTine-startTime)

    def captureStart(self) :
        print("captureStart")
        self.captureTask.start()

    def captureStop(self) :
        print("captureStop")
        self.root.geometry("430x420+800+400")
        self.root.update()

        self.captureTask.stop()


def captureWidget(socketio_obj):
    root = Tk()
    capture_widget = CaptureGUI(root, socketio_obj)
    root.mainloop()

# 소켓과 일차적으로 유저 정보를 받아오는 통신을 진행. 유저 정보 및 플리 저장시킬 그룹 선택 값을 서버에서 받아온다.
def userCheck(userIp) :
            my_client = MyClient(userIp)
            while True :
                try :
                    if my_client.playlistId != None :
                        my_client.send_clientId(my_client.userIp)
                        return captureWidget(my_client)
                except : pass
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
    # local 테스트
    url = "https://43bf-106-241-78-77.ngrok-free.app"
    public_ip = extract_ip_from_uri(url)
    # 실제 배포 시
    # public_ip = await get_public_ip()
    if public_ip is not None:
        print(f"IP 주소: {public_ip}")
        webbrowser.open(url)
        userCheck(public_ip)

if __name__ == "__main__":
    asyncio.run(main())

