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

client.execute("select count(*) from slb_monitor.slb_monitor_data_local")
client.execute("select count(*) from slb_monitor.slb_monitor_data_all")
client.execute("select count(*) from slb_monitor.slb_monitor_data_all where listen_id = '0a20d2c2-4268-11ee-9dd0-c2e5e223b0cb'")
client.execute("select * from slb_monitor.slb_monitor_data_all where listen_id = '0a20d2c2-4268-11ee-9dd0-c2e5e223b0cb' order by time desc limit 5;")

query_sql = "select time, sum(active_conn), sum(in_active_conn) from slb_monitor_data_all where " \
            "listen_id = %(listen_id)s and vm_id in %(vm_ids)s and time >= %(start_time)s and " \
            "time < %(end_time)s group by time order by time;"

params = {
    'listen_id': "0a20d2c2-4268-11ee-9dd0-c2e5e223b0cb",
    'vm_ids': ('a74f7ece-4252-11ee-bd6b-1a45ced73314', 'cd00593c-424c-11ee-bedc-ea9264fa4865'),
    'start_time': '2023-08-24 18:21:50',
    'end_time': '2023-08-25 10:58:45',
}
client.execute(query_sql, params)
