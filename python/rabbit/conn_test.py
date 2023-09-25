import pika

# 建立socket连接
credentials = pika.PlainCredentials("cds_test", "JHasAs1ws88")
connection = pika.BlockingConnection(pika.ConnectionParameters("103.229.215.202", credentials=credentials))
# 建立rabbitMQ协议的通道
channel = connection.channel()
# 声明队列：通过通道申明队列
channel.queue_declare(queue="abc")
# 发送、发布消息：routing_key--队列名称，body--消息
channel.basic_publish(exchange="",
                      routing_key="abc",
                      body="this is a message.")
print ("[x] sent a message.")
# 关闭socket连接
connection.close()