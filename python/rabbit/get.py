import pika

# 建立socket连接
credentials = pika.PlainCredentials("cds_test", "JHasAs1ws88")
connection = pika.BlockingConnection(pika.ConnectionParameters("103.229.215.202", credentials=credentials))
# 建立rabbitMQ协议的通道
channel = connection.channel()
# 声明队列：通过通道申明队列
channel.queue_declare(queue="abc")


# ch：rabbitMQ通道。method:附带的一些参数，类型http的头信息。properties属性。body：消息体。
def callback(ch, method, properties, body):
    print("received [x] message: %r" % ch, method, property, body)


# 接收消息：routing_key--队列名称，body--消息
channel.basic_consume(callback, queue="abc", no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
