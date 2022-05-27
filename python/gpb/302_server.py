from socket import *
from datetime import datetime
import time


def send_message(message):
    server_name = '127.0.0.1'
    server_port = 8877
    info_num = 100000
    print('开始向 {} : {} 发送 {} 条信息!'.format(server_name, server_port, info_num))
    client_socket = socket(AF_INET, SOCK_DGRAM)
    for _ in range(info_num):
        client_socket.sendto(message, (server_name, server_port))
    client_socket.close()

serverPort = 8888
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('port : {} Waiting for connection...'.format(serverPort))
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('{} -- 接收到一条信息, client address : {}'.format(datetime.now(), clientAddress))
    # print(message)
    # send_message(message)
    # time.sleep(1)