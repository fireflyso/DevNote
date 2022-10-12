from clickhouse_driver import Client
import random
from datetime import datetime, timedelta

CK_HOST = "10.2.10.30"
CK_USER = "default"
CK_PASSWORD = "cds-china"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

# client.execute("show databases")
# res = client.execute("SELECT * FROM flow_snmp.flow_data_first_all  where pipe_id = '8d902306-4e5e-11ec-993b-42b493c33671' order by time limit 10")
# print('read update')
# res = client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data where pipe_id  = '3a9a9ff8-b710-11ec-9bfc-8252cbfa8cce' and time >= '2022-04-13 17:45:01' and time < '2022-04-13 17:46:01' order by time")
# print(res)

start_time = datetime.strptime('2022-08-15 00:00:00', '%Y-%m-%d %H:%M:%S')
end_time = datetime.strptime('2022-08-20 00:00:00', '%Y-%m-%d %H:%M:%S')

node_id = 401
operator_ids = [323,324,325,326,327,328,329,330,331,332,679,680,681,684,685]
while start_time < end_time:
    insert_sql = f"insert into wan_fping.rtt_data_v3_20228 (src_ip, dst_ip, ping_time, rtt, node_id, operator_id, asn, trace_type) VALUES"
    add_list = []
    for operator_id in operator_ids:
        for _ in range(100):
            rtt = random.randint(1000, 9000) / 100
            tmp = {
                'src_ip': '148.153.78.58',
                'dst_ip': '79.104.34.189',
                'ping_time': start_time,
                'rtt': rtt,
                'node_id': node_id,
                'operator_id': operator_id,
                'asn': '3216',
                'trace_type': 2,
            }
            add_list.append(tmp)

    client.execute(insert_sql, add_list)
    start_time += timedelta(minutes=30)
    print('time : {} count : {}'.format(start_time, len(add_list)))
