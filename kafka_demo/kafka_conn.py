#!/usr/bin/python3
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json
import random
from datetime import datetime
KAFKA_HOST = '103.229.214.35'
KAFKA_PORT = '9092'

def get_producer():
    return KafkaProducer(
        bootstrap_servers=['{}:{}'.format(KAFKA_HOST, KAFKA_PORT)],
        key_serializer=lambda k: json.dumps(k).encode(),
        value_serializer=lambda v: json.dumps(v).encode()
    )


def get_consumer(topic):
    return KafkaConsumer(
        topic=topic,
        bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT),
        group_id='test',
        key_deserializer=lambda k: json.loads(k).encode(),
        value_deserializer=lambda v: json.loads(v).encode()
    )


def on_send_error(excp):
    print("kafka数据推送失败 : {}".format(excp))


def send_message(producer, message_list, topic):
    if not message_list:
        return

    for message in message_list:
        try_count = 0
        while try_count <= 3:
            try:
                producer.send(topic, message, partition=0)
                break
            except Exception as e:
                try_count += 1
                producer = get_producer()


def get_message(topic):
    producer = get_pro_kafka()
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT), group_id='test',
        enable_auto_commit=True,

    )
    count = 0
    for message in consumer:
        value = eval(message.value.decode('utf-8'))
        count += 1
        if count % 10 == 0:
            print("{} : {}".format(datetime.now(), value))
        producer.send(topic, value, partition=random.randint(0, 4)).add_errback(on_send_error)
        producer.send(topic=topic, key='device_name', value=value).add_errback(on_send_error)



def get_pro_kafka():
    return KafkaProducer(
        bootstrap_servers=['{}:{}'.format('10.216.142.101', 9093)],
        key_serializer=lambda k: json.dumps(k).encode(),
        value_serializer=lambda v: json.dumps(v).encode()
    )


def show_info(topic):
    consumer = KafkaConsumer(topic, bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT), group_id='test')
    partitions = [TopicPartition(topic, p) for p in consumer.partitions_for_topic(topic)]
    toff = consumer.end_offsets(partitions)
    for key in toff.keys():
        print("firefly kafka partition : {}, message count : {}".format(key.partition, toff[key]))

    # consumer = KafkaConsumer(topic, bootstrap_servers='{}:{}'.format('10.216.142.101', 9093), group_id='test')
    # partitions = [TopicPartition(topic, p) for p in consumer.partitions_for_topic(topic)]
    # toff = consumer.end_offsets(partitions)
    # for key in toff.keys():
    #     print("pro kafka partition : {}, message count : {}".format(key.partition, toff[key]))


if __name__ == '__main__':
    # from config.settings import KAFKA_TOPIC_CISCO, KAFKA_TOPIC_HUAWEI, KAFKA_TOPIC_JUNIPER
    # get_message(KAFKA_TOPIC_JUNIPER)
    producer = get_producer()
    res = producer.send(topic='firefly', value='test info', partition=0)
    show_info('firefly')
