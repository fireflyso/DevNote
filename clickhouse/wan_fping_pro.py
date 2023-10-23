from clickhouse_driver import Client

CK_HOST = "10.13.124.35"    # 节点1
CK_HOST = "10.13.124.36"    # 节点2
CK_HOST = "10.13.124.37"    # 节点0
CK_USER = "default"
CK_PASSWORD = "$nM*Jgkx%DmU"
CK_DB_ANME = "wan_fping"
CK_PORT = 9000
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)
client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)
client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)

client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)
client.execute("INSERT INTO wan_fping.mtr_route_local (src_ip, dst_ip, update_time, route) VALUES ('140.210.95.1', '24.103.193.20', '2023-01-05 04:13:54', '');")
client.execute("INSERT INTO wan_fping.mtr_time_local (src_ip, dst_ip, mtr_time, delay) VALUES ('1.1.1.1', '208.210.145.97', '2023-01-04 21:14:04', 3.3);")

client = Client(host="10.13.124.36", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)
client.execute("INSERT INTO wan_fping.mtr_route_local (src_ip, dst_ip, update_time, route) VALUES ('140.210.95.1', '24.103.193.20', '2023-01-05 04:13:54', '');")
client.execute("INSERT INTO wan_fping.mtr_time_local (src_ip, dst_ip, mtr_time, delay) VALUES ('1.1.1.1', '208.210.145.97', '2023-01-04 21:14:04', 3.3);")

client = Client(host="10.13.124.37", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)
client.execute("INSERT INTO wan_fping.mtr_route_local (src_ip, dst_ip, update_time, route) VALUES ('140.210.95.1', '24.103.193.20', '2023-01-05 04:13:54', '');")
client.execute("INSERT INTO wan_fping.mtr_time_local (src_ip, dst_ip, mtr_time, delay) VALUES ('1.1.1.1', '208.210.145.97', '2023-01-04 21:14:04', 3.3);")


client.execute("select country_code, toStartOfTenMinutes(ping_time) as time, avg(delay) from wan_fping.fping_data_all where src_ip = toIPv4('164.52.42.110') and delay > 0 and ping_time >= '2023-01-27 10:55:04' and ping_time <= '2023-01-28 10:55:10' and country_code in ('JP') group by country_code, time")
client.execute("select operator_id, toStartOfTenMinutes(ping_time) as time, avg(delay) from wan_fping.fping_data_all where src_ip = toIPv4('164.52.42.110') and delay > 0 and ping_time >= '2023-01-27 10:55:04' and ping_time <= '2023-01-28 10:55:10' and country_code = 'JP' group by operator_id, time")
client.execute("select country_code, count(*) from wan_fping.fping_data_all where src_ip = toIPv4('164.52.42.110') and delay > 0 and ping_time >= '2023-01-27 10:55:04' and ping_time <= '2023-01-28 10:55:10' group by country_code")

client.execute("select * from wan_fping.fping_data_all where src_ip = toIPv4('164.52.42.110') and dst_ip = toIPv4('160.248.0.32') and ping_time > '2023-02-08 10:57:41' order by ping_time desc limit 1;")

client.execute("select src_ip, avg(delay), median(delay), stddevPop(delay), quantileExact(0.95)(delay) from wan_fping.fping_data_all where (src_ip = toIPv4('148.153.65.178') or src_ip = toIPv4('164.52.2.166')) and delay > 0 and ping_time >= '2023-02-23 10:20:00' and ping_time < '2023-02-23 16:20:00' and country_code = 'KR' group by src_ip;")

client.execute("select count(*) from wan_fping.mtr_route_local")
client.execute("select count(*) from wan_fping.mtr_route_all")

client.execute("select count(*) from wan_fping.mtr_time_local")
client.execute("select count(*) from wan_fping.mtr_time_all")


client.execute("select country_code, avg(delay), median(delay), stddevPop(delay), quantileExact(0.95)(delay) from wan_fping.fping_data_all where src_ip = toIPv4('164.52.42.110') and delay > 0 and ping_time >= '2023-03-15 00:00:00' and ping_time <= '2023-03-16 00:00:00' and country_code in ('KR', 'KR') group by country_code;")
client.execute("select country_code, avg(delay), quantileExact(delay), stddevPop(delay), quantileExact(0.95)(delay) from wan_fping.fping_data_all where src_ip = toIPv4('164.52.42.110') and delay > 0 and ping_time >= '2023-03-15 00:00:00' and ping_time < '2023-03-16 00:00:00' and country_code in ('KR', 'KR') group by country_code;")



client.execute("select * from slb_monitor.slb_monitor_data_local")
client.execute("select * from slb_monitor.slb_monitor_data_all")
client.execute("select * from slb_monitor.slb_monitor_data_all where listen_id = '01e83bcc-e273-11ed-9a6f-ba2442b8b254' order by time desc limit 5;")
client.execute("select time, sum(all_conn), sum(new_conn) from slb_monitor.slb_monitor_data_all where vm_id = '0d57ec54-d919-11ed-b45d-4eb1f1b241d9' group by time order by time desc limit 5;")

client.execute("select * from slb_monitor.slb_monitor_data_all where time > '2023-10-12 11:00:30' and vm_id = '813bae80-eedb-11ed-8ea9-6ed0afc47729' order by time desc limit 3")
client.execute("select * from slb_monitor.slb_monitor_data_all where time > '2023-10-12 11:00:30' order by time desc limit 3")


client.execute("select * from wan_fping.fping_data_all where src_ip = IPv4Address('42.115.66.38') order by ping_time limit 1")
client.execute("select * from wan_fping.fping_data_all where src_ip = toIPv4('164.52.42.110') order by ping_time limit 1")

client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('wan_fping')) AND (table IN ('fping_data_local'))")
client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('wan_fping')) AND (table IN ('mtr_route_local'))")
client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('wan_fping')) AND (table IN ('mtr_time_local'))")

client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('slb_monitor')) AND (table IN ('slb_monitor_data_local'))")

client.execute("SHOW CREATE TABLE slb_monitor.slb_monitor_data_local")


