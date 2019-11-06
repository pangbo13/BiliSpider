from threading import Thread
import socket
from json import dumps as json_dumps
class BilispiderSocket(Thread):
    def __init__(self, HOST, PORT, father):
        super().__init__()
        self.name = "SpiderSocket"
        self.HOST = HOST
        self.PORT = PORT
        self.father = father
        self.logger = father._logger
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.server_socket.connect((self.HOST,self.PORT))
            self.send("spider_connect")
        except Exception:
            print('Server not found or not open')

    # def start_listen(self):
    #     Thread(target=self.receive).start()

    def run(self):
        self.connect()
        while True:
            try:
                data = self.server_socket.recv(1024).decode()
            except ConnectionResetError:
                print("....")
                return
            request_start_line,request_content = data.split("\n",1)
            if "BilispiderSocket" not in request_start_line:
                self.send("not support")
            else:
                msg_id = int(request_start_line.split("/")[-1])
                self.logger.debug("tcp请求id:"+str(msg_id))
                if "get_status" in request_content:
                    self.send(json_dumps(self.father.status),msg_id)

    def send(self,msg,msg_id = 0):
        data = "BilispiderSocket /{} \n{}".format(msg_id,msg).encode()
        Thread(target=self.server_socket.send,args=(data,),name="socketsender").start()


    def close(self):
        self.server_socket.close()
