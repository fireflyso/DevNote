# -- coding: utf-8 --
# @Time : 2023/11/15 11:38
# @Author : xulu.liu
import random

from clickhouse_driver import Client
from datetime import datetime, timedelta
# host 10.4.19.108,10.4.19.109,10.4.19.112
CK_HOST = "10.4.19.112"
CK_USER = "default"
CK_PASSWORD = ""
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

insert_list = []
start_time = datetime.strptime('2024-01-03 00:00:00', '%Y-%m-%d %H:%M:%S')
for _ in range(1000):
    insert_list.append({
        "pipe_id": '',
        "time": start_time,
        "in_flow": 0,
        "out_flow": 0,
        "in_bps": random.randint(50, 100) * 1024 * 1024,
        "out_bps": random.randint(10, 40) * 1024 * 1024
    })
    start_time += timedelta(minutes=5)
insert_sql = "insert into flow_snmp.flow_data_first_local (pipe_id, time, in_flow, out_flow, in_bps, out_bps) values"
client.execute(insert_sql, insert_list)
