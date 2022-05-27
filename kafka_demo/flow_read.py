from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import time
import pymysql

# 打开数据库连接
db = pymysql.connect(
    host="103.229.214.35",
    user="firefly",
    password="cds-cloud@2017",
    database="flow_data",
    port=3306
)
cursor = db.cursor()

sql = "INSERT INTO juniper_flow_data(device_name, interface_name, in_octets, out_octets, time) VALUES (%s,%s,%s,%s,%s)"

consumer = KafkaConsumer(
    'telemetry_message_juniper',
    bootstrap_servers='{}:{}'.format('49.232.142.109', 9092),
    group_id='test05'
)

insert_count = 0
data_list = []
for message in consumer:
    value = eval(message.value.decode('utf-8'))
    # print(value)
    if value.get('type', '') != 'flow':
        continue

    data = (
        value.get('device_name', ''),
        value.get('interface_name', ''),
        value.get('in_octets', ''),
        value.get('out_octets', ''),
        time.localtime(int(value.get('time', '1609430400000')/1000))
    )
    data_list.append(data)
    if len(data_list) >= 1000:
        try:
            cursor.executemany(sql, tuple(data_list))
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
        else:
            insert_count += 1000
            print('累计插入 {} 条数据'.format(insert_count))
        finally:
            data_list = []

