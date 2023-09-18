# -- coding: utf-8 --
# @Time : 2023/8/21 18:30
# @Author : xulu.liu
from clickhouse_driver import Client

CK_USER = "default"
CK_PASSWORD = ""
CK_PORT = 9000

client = Client('10.4.19.108', alt_hosts='10.4.19.109,10.4.19.112', user=CK_USER, password=CK_PASSWORD, round_robin=True)

for _ in range(6):
    res = client.execute("show databases")
    for r in res:
        if 'node' in r[0]:
            print(r[0])
# client.execute("create database node03")
