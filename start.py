import webbrowser
import socketio

# sio = socketio.Client()
# sio.connect('http://localhost:3306')

# @sio.on('connect')
# def on_connect():
#     print('서버 연결')

# @sio.on('check')
# def on_chek(data):
#     print("서버로 전달한 데이터 확인 %s" % data)

# @sio.on('state')
# def on_state(data):
#     print("소켓 연결 상태 : %s" %data)

# @sio.on('user')
# def on_state(data):
#     global user
#     print("연결된유저 : %s" %data)
#     user = data
# def send_data(data):
#     sio.emit('text', data)

# def disconnect(self):
#     sio.disconnect()

class MyClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:3306')
        self.user=None
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
    
    def send_data(self,data):
        self.sio.emit('text', data)

    def disconnect(self):
        self.sio.disconnect()
