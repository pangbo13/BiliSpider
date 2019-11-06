# coding:utf-8

########
# 参考：https://www.cnblogs.com/xinyangsdut/p/9099623.html
########

import socket
import re
import psutil
import json

from threading import Thread

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"


class HTTPServer(object):
    def __init__(self,father):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.father = father
        self.exit_mes = False

    def start(self):
        self.server_socket.listen(128)
        while not self.exit_mes:
            client_socket = self.server_socket.accept()[0]
            handle_client_process = Thread(
                target=self.handle_client, args=(client_socket,))
            handle_client_process.start()

    def handle_client(self, client_socket,):
        """
        处理客户端请求
        """
        # 获取客户端请求数据
        request_data = client_socket.recv(1024).decode()
        request_lines = request_data.splitlines()
        if len(request_lines) > 0:
            # 解析请求报文
            request_start_line = request_lines[0]
        else:
            client_socket.close()
            return
        # 设置响应头
        response_headers = "Server: BiliSpider server\r\n"\
        "Access-Control-Allow-Origin:*\r\n"\
        "Access-Control-Allow-Method:POST,GET\r\n"
        
        # 提取用户请求的文件名
        file_name = re.match(
            r"\w+ +(/[^ ]*) ", request_start_line).group(1)

        if "/" == file_name:
            file_name = "/index.html"

        if len(file_name) >= 5 and file_name[:5] == '/data':
            response_start_line = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type: application/json\r\n"
            response_body = json.dumps({'sys': self.get_sysinfo(),
                                        'spider': self.father.status,
                                        },indent=4)
        elif len(file_name) >= 5 and file_name[:5] == '/exit':
            response_body = 'received exit command!'
            self.exit_mes = True
            from time import sleep
            response_start_line = "HTTP/1.1 200 OK\r\n"
        else:
            # 打开文件，读取内容
            try:
                file = open(HTML_ROOT_DIR + file_name, "rb")
            except IOError:
                response_start_line = "HTTP/1.1 404 Not Found\r\n"
                response_body = "The file is not found!"
            else:
                file_data = file.read()
                file.close()
                # 构造响应数据
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_body = file_data

        if isinstance(response_body,bytes):
            pass
        elif isinstance(response_body,str):
            response_body = response_body.encode('utf_8')
        else:
            response_body = str(response_body).encode('utf_8')

        response = bytes(response_start_line + response_headers + "\r\n" , 'utf-8')+ response_body

        # 向客户端返回响应数据
        client_socket.send(response)

        # 关闭客户端连接
        client_socket.close()

    def bind(self, port):
        self.server_socket.bind(("", port))

    @classmethod
    def get_sysinfo(self):
        # 获取内存信息
        mem_keys = ('total', 'available', 'percent', 'used', 'free')
        mem_svmem = psutil.virtual_memory()
        mem_info = {}
        for i in range(len(mem_keys)):
            mem_info[mem_keys[i]] = mem_svmem[i]
        # 获取CPU使用率
        cpu_info = {'usage': psutil.cpu_percent(percpu=True)}
        # 获取网络IO
        net_keys = ('bytes_sent', 'bytes_recv', 'packets_sent',
                    'packets_recv', 'errin', 'errout', 'dropin', 'dropout')
        net_snetio = psutil.net_io_counters()
        net_info = {}
        for i in range(len(net_keys)):
            net_info[net_keys[i]] = net_snetio[i]

        sys_info = {'mem': mem_info, 'cpu': cpu_info, 'net': net_info}

        return sys_info



def start_server(spider,port=1214):
    http_server = HTTPServer(spider)
    http_server.bind(port)
    http_server.start()


if __name__ == "__main__":
    start_server({})
