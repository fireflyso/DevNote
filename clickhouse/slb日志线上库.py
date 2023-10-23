# -- coding: utf-8 --
# @Time : 2023/8/25 10:24
# @Author : xulu.liu
from clickhouse_driver import Client

client = Client(
    "10.13.134.26",
    alt_hosts="10.13.134.27,10.13.134.28",
    user="slb_monitor_new",
    password="nMAAaaJgkx12DmU",
    database="slb_monitor",
    round_robin=True
)

client.execute("SHOW CREATE TABLE slb_monitor.slb_monitor_data_local")
client.execute("SHOW CREATE TABLE slb_monitor.slb_listen_ping_local")

client.execute("select count(*) from slb_monitor.slb_listen_ping_all")
client.execute("select * from slb_monitor.slb_monitor_data_all where  vm_id in ('03109e84-ef09-11ed-bfd5-6ed0afc47729', 'e7251b83-f579-444d-b402-6e0c37ee03d0', '813bb02e-eedb-11ed-8ea9-6ed0afc47729', '4c862e4c-2346-4a29-aec0-3ef6c7e3e8fe', '813bae80-eedb-11ed-8ea9-6ed0afc47729', 'fd62b1fe-4709-4272-9468-8df44a3de246') order by time desc limit 3")
client.execute("select * from slb_monitor.slb_monitor_data_all order by time desc limit 3")
client.execute("select count(*) from slb_monitor.slb_monitor_data_all where listen_id = '0a20d2c2-4268-11ee-9dd0-c2e5e223b0cb'")
client.execute("select * from slb_monitor.slb_listen_ping_all where slb_id = 'fac2b190-ef12-11ed-9699-aafb37de4739' order by time desc limit 5;")


query_sql = "select listen_id, time, sum(active_conn), sum(in_active_conn) from slb_monitor_data_all where listen_id in %(listen_ids)s and vm_id in %(vm_ids)s and time > %(last_5)s group by listen_id, time order by time;"
from datetime import datetime, timedelta
last_5 = datetime.now() - timedelta(minutes=5)
params = {
    'listen_ids': ('e84b5f40-57a8-11ee-a942-ba11c4fa0c1d', '168b76ce-579a-11ee-8f76-92fb8eaf2ec9'),
    'vm_ids': ('f745aac2-55fb-11ee-8367-ce4feaf07182', 'f745aac2-55fb-11ee-8367-ce4feaf07182'),
    'last_5': last_5}
client.execute(query_sql, params)
