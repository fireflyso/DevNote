# coding=utf-8
from clickhouse_driver import Client
from datetime import datetime

CK_HOST = "10.13.133.133"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
start_time = datetime.now()
print('开始进行数据迁移...')
client.execute("insert into flow_snmp.flow_data_local_new select * from remote('10.13.133.133',flow_snmp.flow_data_local_new_v1,'flowdata','wVen6RK3KpkpGdsA')")
print("数据迁移完成，用时：{} s".format((datetime.now() - start_time).seconds))


# [(644258906, u'31.20 GiB', u'7.53 GiB')]
# [(705357846, u'47.95 GiB', u'22.74 GiB')]
