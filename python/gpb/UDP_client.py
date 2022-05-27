from socket import *

def send_message(message):
    server_name = '127.0.0.1'
    server_port = 8877
    print('开始向 {} : {} 发送一条信息!'.format(server_name, server_port))
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.sendto(message, (server_name, server_port))
    client_socket.close()