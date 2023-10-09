import pika
import time

import utils_logger

logger = utils_logger.get_logger('mq', 'INFO')

# 自己买的华为云
conf = {
    'host': '120.46.67.226',
    'port': 5672,
    'queue_name': 'queue-test',
    'username': 'zq_meituan_mq',
    'password': '2TKNXVQYS8Ys2Cm'
}

# 客户提供
conf = {
    'host': '120.46.84.57',
    'port': 5672,
    'queue_name': 'queue-test',
    'username': 'rabbit',
    'password': 'HPImGcj3C6CnMqKY'
}

credentials = pika.PlainCredentials(conf['username'], conf['password'])
parameters = pika.ConnectionParameters(conf['host'],
                                       conf['port'],
                                       '/',
                                       credentials,
                                       heartbeat=5)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(conf['queue_name'])

for index in range(86400):
    data = bytes("data {}!".format(index), encoding="utf-8")
    channel.basic_publish(exchange='', routing_key=conf['queue_name'], body=data)
    logger.info('push {}'.format(index))
    time.sleep(1)

print(" [x] Sent 'Hello World!'")

connection.close()
