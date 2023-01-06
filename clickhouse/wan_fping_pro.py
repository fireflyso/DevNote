from clickhouse_driver import Client
from datetime import datetime, timedelta

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


client.execute("select count(*) from wan_fping.fping_data_all")

client.execute("select count(*) from wan_fping.mtr_route_local")
client.execute("select count(*) from wan_fping.mtr_route_all")

client.execute("select count(*) from wan_fping.mtr_time_local")
client.execute("select count(*) from wan_fping.mtr_time_local")






