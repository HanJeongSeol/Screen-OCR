import time
import threading
from tkinter import *
from pororo import Pororo
import numpy as np
import cv2
from PIL import ImageGrab
import socketio

global cnt
cnt = 0

class MyClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:3306')
        self.user

        @self.sio.on('connect')
        def on_connect():
            print('서버 연결')
        
        @self.sio.on('check')
        def on_chek(data):
            print("서버로 전달한 데이터 확인 %s" % data)
        
        @self.sio.on('state')
        def on_state(data):
            print("소켓 연결 상태 : %s" %data)
    
    def send_data(self,data):
        self.sio.emit('text', data)

    def disconnect(self):
        self.sio.disconnect()
            
myCli = MyClient()
