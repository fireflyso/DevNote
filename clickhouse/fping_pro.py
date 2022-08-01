from clickhouse_driver import Client
from datetime import datetime, timedelta

CK_HOST = "10.13.124.35"
CK_HOST = "10.13.124.37"
CK_USER = "default"
CK_PASSWORD = "$nM*Jgkx%DmU"
CK_DB_ANME = "f_ping"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data_first_all where pipe_id  = '6c6d7e6a-2375-11e9-9cc0-0242ac110002' and time >= '2021-06-30 12:30:00' and time <= '2021-06-30 16:55:00' order by time")


sql = "CREATE TABLE flow_snmp.flow_data_local_new_second (`pipe_id` String,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=Log"
ans = client.execute(sql)

client.execute("SHOW TABLES FROM f_ping")
client.execute("SHOW databases")
client.execute("SHOW GRANTS")
client.execute("SELECT * FROM system.clusters")
client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data where pipe_id  = '3a9a9ff8-b710-11ec-9bfc-8252cbfa8cce' and time >= '2022-04-13 17:45:01' and time < '2022-04-13 17:46:01' order by time")
# 查看表中数据条数以及空间占用情况
client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('f_ping')) AND (table IN ('rtt_data_20227'))")
client.execute("SELECT pipe_id from flow_snmp.flow_data_local_new where time > '2021-05-01 12:00:00' order by time limit 50")
client.execute("SELECT pipe_id, COUNT(pipe_id) FROM flow_snmp.flow_data_local_new where time > '2021-07-06 11:00:00' group by pipe_id")
client.execute("SELECT pipe_id, COUNT(pipe_id) FROM flow_snmp.flow_data_local_new where time > '2020-10-06 11:00:00' and time > '2020-10-06 12:00:00' group by pipe_id")




client.execute("SELECT time, in_bps, out_bps from flow_snmp.flow_data WHERE pipe_id  = '06be7cce-c55d-11e9-82db-0242ac110002' and time > '2021-06-06 12:30:00' and time < '2021-07-06 12:30:00' order by time")


client.execute("select * from f_ping.rtt_data_20227 where src_ip = '43.130.1.192' limit 10")

base_str = """
            from
                {0}
            where 
                rtt>0 and ping_time>='{1}' and ping_time<'{2}' and src_ip='{3}' and operator_id in ({4}) and 
                node_id in ({5}) and trace_type={6} 
            GROUP BY node_id, operator_id 
            ORDER BY node_id ,operator_id""".format('f_ping.rtt_data_v3_20227', '2022-07-28 00:00:00', '2022-07-28 06:00:00',
                                                    '43.130.1.192', '263', '396',
                                                    '2')

rtt_query = """
            select 
                operator_id,
                node_id, 
                AVG(rtt) as rtt_avg,
                MAX(rtt) as rtt_max,
                MIN(rtt) as rtt_min,
                stddevPop(rtt) as rtt_std,
                median(rtt) as rtt_median,
                quantileExact(0.95)(rtt) as rtt_q95,
                sum(case when rtt>=0 and rtt<50 then 1 else 0 end)/count(0) as rtt_0,
                sum(case when rtt>=50 and rtt<80 then 1 else 0 end)/count(0) as rtt_50,
                sum(case when rtt>=80 and rtt<100 then 1 else 0 end)/count(0) as rtt_80,
                sum(case when rtt>=100 and rtt<120 then 1 else 0 end)/count(0) as rtt_100,
                sum(case when rtt>=120 and rtt<150 then 1 else 0 end)/count(0) as rtt_120,
                sum(case when rtt>=150 and rtt<200 then 1 else 0 end)/count(0) as rtt_150,
                sum(case when rtt>=200 then 1 else 0 end)/count(0) as rtt_200
            %s;
            """ % base_str

client.execute(rtt_query)
avg_rtt_query = "select AVG(rtt) from f_ping.rtt_data_v3_20227 where rtt>0 and ping_time>='2022-07-28 00:00:00' and ping_time<'2022-07-28 06:00:00' and src_ip='43.130.1.192' and operator_id in (263) and node_id in (396) and trace_type=2"

avg_rtt_query = "select AVG(rtt) from f_ping.rtt_data_v3_20227 where rtt>0 and rtt<=600 and ping_time>='{}' and ping_time<'{}' and src_ip='104.166.128.58' and operator_id in (324) and node_id in (401) and trace_type=2".format(start_time, start_time + timedelta(hours=6))










