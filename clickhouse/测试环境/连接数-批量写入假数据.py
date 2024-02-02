# -- coding: utf-8 --
# @Time : 2023/11/3 17:23
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
start_time = datetime.strptime('2023-11-03 00:00:00', '%Y-%m-%d %H:%M:%S')
for _ in range(1000):
    insert_list.append({
        "vm_id": '015b23ef-34e7-11ee-8f42-00505684ba28',
        "listen_id": 'd17f256a-7898-11ee-90d1-da52db55ee96',
        "time": start_time,
        "all_conn": random.randint(900, 1100)
    })
    start_time += timedelta(minutes=1)
insert_sql = "insert into slb_monitor.slb_monitor_data_local (vm_id, listen_id, time, all_conn) values"
client.execute(insert_sql, insert_list)
