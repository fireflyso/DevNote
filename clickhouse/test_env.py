from clickhouse_driver import Client
import random
from datetime import datetime, timedelta

CK_HOST = "10.4.19.112"
CK_USER = "default"
CK_PASSWORD = ""
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

client.execute("show databases")
client.execute("desc flow_snmp")
breakpoint()
# client.execute("select version()")
# client.execute("select * from system.clusters")

# breakpoint()
# client.execute("SELECT name FROM system.tables WHERE database = 'slb_monitor'")
# client.execute("show create table slb_monitor.slb_listen_ping_local")
# client.execute("CREATE TABLE slb_monitor.slb_monitor_data_all ( `vm_id` UUID comment 'DPVS机器ID', `listen_id` UUID comment '监听ID', `time` DateTime comment '采集时间', `active_conn` UInt32 comment '活跃连接数', `in_active_conn` UInt32 comment '非活跃连接数', `new_conn` UInt64 comment '新增连接数', `loss_conn` UInt64 comment '丢失连接数', `all_conn` UInt64 comment '累计连接数', `in_pkts` UInt64 comment '入向数据包数', `out_pkts` UInt64 comment '出向数据包数', `in_bits` UInt64 comment '入向带宽bit', `out_bits` UInt64 comment '出向带宽bit', `all_in_pkts` UInt64 comment '累计入向包数', `all_out_pkts` UInt64 comment '累计出向包数', `all_in_bytes` UInt64 comment '累计入向字节数（非bit）', `all_out_bytes` UInt64 comment '累计出向字节数（非bit）' ) ENGINE = Distributed('clickhouse_remote_servers', 'slb_monitor', 'slb_monitor_data_local', rand())")
# client.execute("CREATE TABLE slb_monitor.slb_monitor_data_local (`vm_id` UUID COMMENT 'DPVS机器ID', `listen_id` UUID COMMENT '监听ID', `time` DateTime COMMENT '采集时间', `active_conn` UInt32 COMMENT '活跃连接数', `in_active_conn` UInt32 COMMENT '非活跃连接数', `new_conn` UInt64 COMMENT '新增连接数', `loss_conn` UInt64 COMMENT '丢失连接数', `all_conn` UInt64 COMMENT '累计连接数', `in_pkts` UInt64 COMMENT '入向数据包数', `out_pkts` UInt64 COMMENT '出向数据包数', `in_bits` UInt64 COMMENT '入向带宽bit', `out_bits` UInt64 COMMENT '出向带宽bit', `all_in_pkts` UInt64 COMMENT '累计入向包数', `all_out_pkts` UInt64 COMMENT '累计出向包数', `all_in_bytes` UInt64 COMMENT '累计入向字节数（非bit）', `all_out_bytes` UInt64 COMMENT '累计出向字节数（非bit）') ENGINE = MergeTree PARTITION BY toYYYYMMDD(time) ORDER BY (vm_id, listen_id, time) SETTINGS index_granularity = 8192")
#
# res = client.execute("select toTimeZone(toStartOfFiveMinute(time), '') as time, sum(in_bps), sum(out_bps) from flow_snmp.flow_data_first_all where (pipe_id in ('005e8666-8381-11ea-bda2-dea2ec15d6d8') and time >= '2023-06-01 00:00:00' and time < '2023-07-01 00:00:00') or (pipe_id in ('0109dc00-c73d-11ea-8bf4-4a2e5f6563fe') and time >= '2023-06-01 00:00:00' and time < '2023-07-01 00:00:00') group by time order by time;")
# print(res)
# print('read update')
res = client.execute("SELECT * FROM slb_monitor.slb_monitor_data_all where time >= '2023-11-01 17:45:01'order by time limit 10")
print(res)

# start_time = datetime.strptime('2022-08-15 00:00:00', '%Y-%m-%d %H:%M:%S')
# end_time = datetime.strptime('2022-08-20 00:00:00', '%Y-%m-%d %H:%M:%S')
#
# node_id = 401
# operator_ids = [323,324,325,326,327,328,329,330,331,332,679,680,681,684,685]
# while start_time < end_time:
#     insert_sql = f"insert into wan_fping.rtt_data_v3_20228 (src_ip, dst_ip, ping_time, rtt, node_id, operator_id, asn, trace_type) VALUES"
#     add_list = []
#     for operator_id in operator_ids:
#         for _ in range(100):
#             rtt = random.randint(1000, 9000) / 100
#             tmp = {
#                 'src_ip': '148.153.78.58',
#                 'dst_ip': '79.104.34.189',
#                 'ping_time': start_time,
#                 'rtt': rtt,
#                 'node_id': node_id,
#                 'operator_id': operator_id,
#                 'asn': '3216',
#                 'trace_type': 2,
#             }
#             add_list.append(tmp)
#
#     client.execute(insert_sql, add_list)
#     start_time += timedelta(minutes=30)
#     print('time : {} count : {}'.format(start_time, len(add_list)))
