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
insert_sql = "ALTER TABLE flow_snmp.flow_data_first_local DELETE where pipe_id = '3bfcbbfa-785d-11ee-aa70-5ef935faf398'"
client.execute(insert_sql)
