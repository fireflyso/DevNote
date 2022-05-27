# -*- coding: utf-8 -*-
from clickhouse_driver import Client
from datetime import datetime

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

start_at = datetime.now()

client.execute("RENAME TABLE flow_snmp.flow_data_second_local_v1 TO flow_snmp.flow_data_second_local ON CLUSTER cluster_1shards_3replicas")
client.execute("RENAME TABLE flow_snmp.flow_data_second_local TO flow_snmp.flow_data_first_local ON CLUSTER cluster_1shards_3replicas")

print("修改数据库表名用时 : {} 微秒".format((datetime.now() - start_at).microseconds))
