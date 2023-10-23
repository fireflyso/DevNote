# -- coding: utf-8 --
# @Time : 2023/10/10 18:03
# @Author : xulu.liu
from clickhouse_driver import Client
# host 10.4.19.108,10.4.19.109,10.4.19.112
CK_HOST = "10.4.19.112"
CK_USER = "default"
CK_PASSWORD = ""
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

breakpoint()
# client.execute("show databases")
# client.execute("select version()")
# client.execute("select * from system.clusters")
# client.execute("SELECT name FROM system.tables WHERE database = 'slb_monitor'")
# client.execute("show create table slb_monitor.slb_listen_ping_local")
# client.execute("show create table slb_monitor.slb_listen_ping_all")
# client.execute("select * from slb_monitor.slb_listen_ping_all")
sql = """
CREATE TABLE slb_monitor.slb_listen_ping_local
(
	`slb_id` UUID comment '负载均衡ID',
	`listen_id` UUID comment '实际ping的监听ID',
	`time` DateTime comment '采集时间',
	`delay` Float32 comment '延时数据',
	`loss` Float32 comment '丢包数据',
	`slb_type` String comment 'vdc/vpc'
)
ENGINE = MergeTree
PARTITION BY toYYYYMMDD(time)
ORDER BY (slb_id, listen_id, time)
SETTINGS index_granularity = 8192;
"""

client.execute(sql)

sql = """
CREATE TABLE slb_monitor.slb_listen_ping_all
(
	`slb_id` UUID comment '负载均衡ID',
	`listen_id` UUID comment '实际ping的监听ID',
	`time` DateTime comment '采集时间',
	`delay` Float32 comment '延时数据',
	`loss` Float32 comment '丢包数据',
	`slb_type` String comment 'vdc/vpc'
)
ENGINE = Distributed('cluster_3shards_1replicas', 'slb_monitor', 'slb_listen_ping_local', rand())
"""
client.execute(sql)
