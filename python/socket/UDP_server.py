from socket import *
import logical_port_pb2
from datetime import datetime

serverPort = 8877
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('Waiting for connection...')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('{} -- 接收到一条信息, client address : {}\n\n'.format(datetime.now(), clientAddress))
    print(message)
    try:
        ts = logical_port_pb2.telemetry_top_pb2.TelemetryStream()
        ts.ParseFromString(message)
        print('\n\n解析结果: \n{}'.format(ts))
    except Exception as e:
        print('exception e : {}'.format(e))