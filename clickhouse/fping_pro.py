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




client.execute("select quantileExact(0.95)(rtt) from f_ping.rtt_data_v3_20228 where rtt>0 and ping_time>='2022-08-01 03:00:00' and ping_time<'2022-08-01 04:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 02:00:00' and ping_time<'2022-08-01 03:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 01:00:00' and ping_time<'2022-08-01 02:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 04:00:00' and ping_time<'2022-08-01 05:00:00' and src_ip='104.166.128.58' and operator_id in (684) and node_id in (401) and trace_type=2")


client.execute("select * from f_ping.rtt_data_20228 where ping_time>='2022-08-04 00:00:00' and ping_time<'2022-08-04 02:00:00' and src_ip='104.166.128.58' and node_id = 401 and operator_id in (324,325) limit 1")
client.execute("select * from f_ping.rtt_data_20229 where src_ip='164.52.2.166' order by ping_time desc limit 1")

base_str = """
            from
                {0}
            where 
                rtt>0 and ping_time>='{1}' and ping_time<'{2}' and src_ip='{3}' and operator_id in ({4}) and 
                node_id in ({5}) and trace_type={6} 
            GROUP BY node_id, operator_id 
            ORDER BY node_id ,operator_id""".format('f_ping.rtt_data_v3_20228', '2022-08-04 00:00:00', '2022-08-05 00:00:00',
                                                    '43.130.1.192', '263', '396',
                                                    '2')

base_str = """
            from
                {0}
            where 
                rtt>0 and rtt<=101.56 and ping_time>='{1}' and ping_time<'{2}' and src_ip='{3}' and operator_id in ({4}) and 
                node_id in ({5}) and trace_type={6} 
            GROUP BY node_id, operator_id 
            ORDER BY node_id ,operator_id""".format('f_ping.rtt_data_v3_20228', '2022-08-04 00:00:00', '2022-08-05 00:00:00',
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
avg_rtt_query = "select dst_ip from f_ping.rtt_data_v3_20228 where trace_type=2 order by rtt desc limit 100"

avg_rtt_query = "select AVG(rtt) from f_ping.rtt_data_v3_20227 where rtt>0 and rtt<=600 and ping_time>='{}' and ping_time<'{}' and src_ip='104.166.128.58' and operator_id in (324) and node_id in (401) and trace_type=2".format(start_time, start_time + timedelta(hours=6))
avg_rtt_query = "select MAX(rtt) as rtt_max from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 12:00:00' src_ip='104.166.128.58' and trace_type=2"


client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select node_id, sum(rtt) as total_rtt, sum(case when rtt>0 then 1 else 0 end) as rtt_count, sum(case when rtt=0 then 1 else 0 end)/count(0) as loss from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 00:00:00' and ping_time<'2022-08-02 00:00:00' and src_ip='104.166.128.58' and trace_type=2 group by node_id")
client.execute("select toHour(ping_time) as time, operator_id, sum(rtt), sum(case when rtt>0 then 1 else 0 end), sum(case when rtt=0 then 1 else 0 end)/count(0) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-04 00:00:00' and ping_time<'2022-08-05 00:00:00' and src_ip='104.166.128.58' and node_id = 401 group by time, operator_id order by time desc;")
client.execute("select operator_id, sum(case when rtt=0 then 1 else 0 end)/count(0) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-04 00:00:00' and ping_time<'2022-08-05 00:00:00' and src_ip='104.166.128.58' and node_id = 401 group by operator_id;")


client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(distinct dst_ip) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 17:15:00' and ping_time<'2022-08-01 17:25:00' and src_ip='104.166.128.58' and operator_id in (331) and node_id in (401) and trace_type=2")
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-01 17:15:00' and ping_time<'2022-08-02 17:15:00' and src_ip='104.166.128.58' and operator_id in (331) and node_id in (401) and trace_type=2")
client.execute("select operator_id, node_id, count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-09 00:00:00' and ping_time<'2022-08-10 00:00:00' and src_ip='104.166.128.58' and operator_id in (323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 679, 680, 681, 684, 685) and node_id in (401) and trace_type=2 group by operator_id, node_id")

# 香港BGP 0
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.12.14' and trace_type=2")
client.execute("select MAX(rtt) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.12.14' and trace_type=2")

# 新加坡BGP 2
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.2.166' and trace_type=2")
client.execute("select MAX(rtt) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.2.166' and trace_type=2")

# 东京BPG 1
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.25.158' and trace_type=2")
client.execute("select MAX(rtt) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.25.158' and trace_type=2")

#  首尔BGP 2
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.42.110' and trace_type=2")
client.execute("select MAX(rtt) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 17:15:00' and src_ip='164.52.42.110' and trace_type=2")

# 法兰克福BGP 0
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.82.18' and trace_type=2")
client.execute("select MAX(rtt) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.82.18' and trace_type=2")


# 台北VIP专用带宽 0
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='150.116.92.50' and trace_type=2")
client.execute("select MAX(rtt) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='150.116.92.50' and trace_type=2")


#  孟买BGP 0
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='164.52.120.134' and trace_type=2")


#  阿姆斯特丹BGP 1
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.25.234' and trace_type=2")


#  洛杉矶BGP 2
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.44.206' and trace_type=2")


#  达拉斯VIP专用宽带 1
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.48.206' and trace_type=2")


#  弗吉尼亚BGP 2
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.160.146' and trace_type=2")


#  新加坡东南亚区域优化 1
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='164.52.53.238' and trace_type=2")


#   台北BGP中国优化 0
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='164.52.9.118' and trace_type=2")


#   迈阿密BPG 1
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.168.204' and trace_type=2")


#   新加坡经济型BGP 0
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.146.54' and trace_type=2")


#   新加坡音视频专用带宽 1
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.184.2' and trace_type=2")


#   圣保罗BGP 2
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.200.42' and trace_type=2")


#   胡志明本地多线BGP 0
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='42.115.66.38' and trace_type=2")


#   雅加达多线BGP 1
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select count(*) from f_ping.rtt_data_v3_20228 where ping_time>='2022-08-08 19:05:00' and src_ip='148.153.100.194' and trace_type=2")


#   马赛BGP 2
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select * from f_ping.rtt_data_v3_20228 where src_ip='148.153.78.58' and trace_type=2 order by ping_time desc limit 10")


#   法兰克福-摩洛哥 0
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select * from f_ping.rtt_data_v3_20229 where src_ip='148.153.103.2' and trace_type=2 limit 5")


#   达拉斯覆盖墨西哥 2
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select * from f_ping.rtt_data_v3_202210 where src_ip='148.153.122.6' and trace_type=2 order by ping_time desc limit 5")

#   达拉斯BGP 1
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
client.execute("select * from f_ping.rtt_data_v3_202210 where src_ip='148.153.39.154' and trace_type=2 order by ping_time desc limit 5")


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







