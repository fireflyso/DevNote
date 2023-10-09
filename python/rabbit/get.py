import pika

import utils_logger

logger = utils_logger.get_logger('mq_get', 'INFO')
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
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(conf['queue_name'])


def callback(ch, method, properties, body):
    logger.info(" [x] Received %r" % body.decode('utf-8'))


channel.basic_consume(queue=conf['queue_name'], on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
