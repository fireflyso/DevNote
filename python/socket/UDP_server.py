from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print('Waiting for connection...')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('Receive Message: %s' %message.decode('utf-8'))
    modifiedMessage = message.decode('utf-8').upper()
    serverSocket.sendto(modifiedMessage.encode('utf-8'), clientAddress)
