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

client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('slb_monitor')) AND (table IN ('slb_listen_ping_local'))")

client.execute("select time, sum(all_conn) from slb_monitor.slb_monitor_data_all where listen_id = 'b5b9014e-8201-11ee-a711-56418d35492d' and vm_id in ('83f75abc-81f6-11ee-9668-56f96f14c566', '83f75ff8-81f6-11ee-9668-56f96f14c566', '83f763e0-81f6-11ee-9668-56f96f14c566', '83f7680e-81f6-11ee-9668-56f96f14c566') group by time order by time desc limit 10")
client.execute("select vm_id, time, all_conn from slb_monitor.slb_monitor_data_all where  vm_id in ('83f75ff8-81f6-11ee-9668-56f96f14c566') order by time desc limit 10")

client.execute("SHOW CREATE TABLE slb_monitor.slb_monitor_data_local")
client.execute("SHOW CREATE TABLE slb_monitor.slb_listen_ping_local")

client.execute("select count(*) from slb_monitor.slb_listen_ping_all")
client.execute("select time, sum(all_conn) from slb_monitor.slb_monitor_data_all where listen_id = '4db2b3c8-7e1a-11ee-a8b0-9a3ef970e1c6' and vm_id in ('1a12ac4b-7ddb-11ee-bde6-005056ab54bc', '1a12ac4b-7ddb-11ee-bde6-005056ab54bc') and time >= '2023-11-08 17:36:33' and time < '2023-11-08 18:36:33' group by time order by time")
client.execute("select * from slb_monitor.slb_monitor_data_all where  vm_id = '83f75abc-81f6-11ee-9668-56f96f14c566' order by time desc limit 3")
client.execute("select count(*) from slb_monitor.slb_monitor_data_all where  vm_id = 'fdfa778f-a03a-491b-912b-1484055984f7'")
client.execute("select count(*) from slb_monitor.slb_monitor_data_all where  vm_id = '1a12ac4b-7ddb-11ee-bde6-005056ab54bc'")
client.execute("select * from slb_monitor.slb_monitor_data_all order by time desc limit 3")
client.execute("select count(*) from slb_monitor.slb_monitor_data_all where listen_id = '0a20d2c2-4268-11ee-9dd0-c2e5e223b0cb'")
client.execute("select all_conn from slb_monitor.slb_monitor_data_all where time > '2024-01-16 00:50:15' and listen_id = '10ac3472-b34e-11ee-a391-e6382a5848fd'  order by time desc limit 5;")
client.execute("select time, sum(all_conn) from slb_monitor_data_all where listen_id in ('0548838a-b414-11ee-a80b-0edd79386f86', '10ac3472-b34e-11ee-a391-e6382a5848fd', '13d39a46-b34e-11ee-a391-e6382a5848fd', '2d5df700-b34d-11ee-906e-c6de451cd772', 'f7ea0650-b413-11ee-a80b-0edd79386f86') and vm_id in ('b24af028-97dc-44fa-a306-b8438561b783', 'f2a971e4-ddd8-426b-98bb-0e44859d422d') and time >= '2024-01-16 00:50:15' group by time order by time limit 5;")
client.execute("select time, all_conn, vm_id from slb_monitor_data_all where listen_id = '0548838a-b414-11ee-a80b-0edd79386f86' and time >= '2024-01-16 14:50:00'")


query_sql = "select listen_id, time, sum(active_conn), sum(in_active_conn) from slb_monitor_data_all where listen_id in %(listen_ids)s and vm_id in %(vm_ids)s and time > %(last_5)s group by listen_id, time order by time;"
from datetime import datetime, timedelta
last_5 = datetime.now() - timedelta(minutes=5)
params = {
    'listen_ids': ('e84b5f40-57a8-11ee-a942-ba11c4fa0c1d', '168b76ce-579a-11ee-8f76-92fb8eaf2ec9'),
    'vm_ids': ('f745aac2-55fb-11ee-8367-ce4feaf07182', 'f745aac2-55fb-11ee-8367-ce4feaf07182'),
    'last_5': last_5}
client.execute(query_sql, params)
