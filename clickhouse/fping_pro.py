from clickhouse_driver import Client
from datetime import datetime, timedelta

CK_HOST = "10.13.124.35"    # 节点1
CK_HOST = "10.13.124.36"    # 节点2
CK_HOST = "10.13.124.37"    # 节点0
CK_USER = "default"
CK_PASSWORD = "$nM*Jgkx%DmU"
CK_DB_ANME = "f_ping"
CK_PORT = 9000
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)


client.execute("select count(*) from f_ping.rtt_data_v3_20231 where ping_time>='2023-01-31 12:15:00' and src_ip='118.68.168.129'")

client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data_first_all where pipe_id  = '6c6d7e6a-2375-11e9-9cc0-0242ac110002' and time >= '2021-06-30 12:30:00' and time <= '2021-06-30 16:55:00' order by time")


sql = "CREATE TABLE flow_snmp.flow_data_local_new_second (`pipe_id` String,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=Log"
ans = client.execute(sql)

client.execute("SHOW TABLES FROM f_ping")
client.execute("SHOW databases")
client.execute("SHOW GRANTS")
client.execute("SHOW CREATE f_ping.rtt_data_20228")
client.execute("SHOW CREATE f_ping.rtt_data_v3_20228")
client.execute("SELECT * FROM system.clusters")
# 查看表中数据条数以及空间占用情况
client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('f_ping')) AND (table IN ('rtt_data_v3_20229'))")
client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('slb_monitor')) AND (table IN ('rtt_data_v3_20229'))")




client.execute("select quantileExact(0.95)(rtt) from f_ping.rtt_data_v3_20228 where rtt>0 and ping_time>='2022-08-01 03:00:00' and ping_time<'2022-08-01 04:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 02:00:00' and ping_time<'2022-08-01 03:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 01:00:00' and ping_time<'2022-08-01 02:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 04:00:00' and ping_time<'2022-08-01 05:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")


client.execute("select * from f_ping.rtt_data_20228 where ping_time>='2022-08-04 00:00:00' and ping_time<'2022-08-04 02:00:00' and src_ip='104.166.128.58' and node_id = 401 and operator_id in (324,325) limit 1")
client.execute("select * from f_ping.rtt_data_20229 where src_ip='164.52.2.166' order by ping_time desc limit 1")


avg_rtt_query = "select AVG(rtt) from f_ping.rtt_data_v3_20227 where rtt>0 and ping_time>='2022-07-28 00:00:00' and ping_time<'2022-07-28 06:00:00' and src_ip='43.130.1.192' and operator_id in (263) and node_id in (396) and trace_type=2"
avg_rtt_query = "select dst_ip from f_ping.rtt_data_v3_20228 where trace_type=2 order by rtt desc limit 100"

avg_rtt_query = "select AVG(rtt) from f_ping.rtt_data_v3_20227 where rtt>0 and rtt<=600 and ping_time>='{}' and ping_time<'{}' and src_ip='104.166.128.58' and operator_id in (324) and node_id in (401) and trace_type=2".format(start_time, start_time + timedelta(hours=6))
avg_rtt_query = "select MAX(rtt) as rtt_max from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 12:00:00' src_ip='104.166.128.58' and trace_type=2"



start_time = datetime.strptime('2022-07-27 00:00:00', '%Y-%m-%d %H:%M:%S')
end_time = datetime.strptime('2022-07-28 00:00:00', '%Y-%m-%d %H:%M:%S')
count = 0
total = 0
while start_time < end_time:
    temp_time = start_time + timedelta(hours=1)
    avg_rtt_query = "select AVG(rtt) from f_ping.rtt_data_v3_20227 where rtt>0 and ping_time>='{}' and ping_time<'{}' and src_ip='104.166.128.58' and operator_id in (324) and node_id in (401) and trace_type=2".format(start_time, temp_time)
    # avg_rtt_query = "select AVG(rtt) from f_ping.rtt_data_v3_20227 where rtt>0 and rtt<=127.37 and ping_time>='{}' and ping_time<'{}' and src_ip='104.166.128.58' and operator_id in (324) and node_id in (401) and trace_type=2".format(start_time, temp_time)
    res = client.execute(avg_rtt_query)
    total += res[0][0]
    count += 1
    start_time = temp_time
    print(start_time)







