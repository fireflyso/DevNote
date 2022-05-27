'''
2021年08月24日 这几个pipe由于创建后一分钟就删除了，所以没有统计到flow信息，手动添加了一组0数据
'''
from clickhouse_driver import Client

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('19775da4-4396-11ec-9ce0-96fc12e593c4', '2021-11-12 16:55:15', 0.0, 0.0, 0.0, 0.0)")
client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('a3d15d34-438b-11ec-9640-9e50b3548dd5', '2021-11-12 15:40:16', 0.0, 0.0, 0.0, 0.0)")
client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('f27f6012-438a-11ec-bb30-3a46afcb3361', '2021-11-12 15:35:19', 0.0, 0.0, 0.0, 0.0)")
client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('8d6b321c-438c-11ec-9640-9e50b3548dd5', '2021-11-12 15:46:48', 0.0, 0.0, 0.0, 0.0)")

client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('f5045586-45bf-11ec-8a31-721b06e4bfff', '2021-11-15 10:59:25', 0.0, 0.0, 0.0, 0.0)")

client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('bb7d5456-eeae-11eb-b991-2a07db47f251', '2021-07-27 15:46:50', 0.0, 0.0, 0.0, 0.0)")
client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('da6a9a94-eeaf-11eb-a6ff-46ab5ca77e96', '2021-07-27 15:54:53', 0.0, 0.0, 0.0, 0.0)")

client.execute("select * from flow_snmp.flow_data_local_new where pipe_id = '19775da4-4396-11ec-9ce0-96fc12e593c4'")


from datetime import datetime, timedelta
start_time = datetime(2021, 10, 31, 10, 24, 3)
for _ in range(8640):
    start_time += timedelta(minutes=5)
    client.execute("INSERT INTO flow_snmp.flow_data_local_new (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('35572c14-3894-11ec-8e29-ba6016034d9c', '{}', 0.0, 0.0, 0.0, 0.0)".format(start_time))


