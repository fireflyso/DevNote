from clickhouse_driver import Client

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

start_time = '2022-11-24 16:19:00'
end_time = '2022-12-07 14:25:00'

src_pipe_id = '9b2c873e-cb5c-446f-8163-3eb54e4f6c27'
dst_pipe_id = '5a9aa7b4-bffd-11ea-8115-0242ac110002'

res = client.execute(
    "SELECT time, in_flow, out_flow, in_bps, out_bps FROM flow_snmp.flow_data where pipe_id  = '{}' and time >= '{}' and time < '{}' order by time".format(
        src_pipe_id, start_time, end_time))
data_list = []
for r in res:
    temp = list(r)
    temp.insert(0, dst_pipe_id)
    data_list.append(temp)

insert_sql = f"insert into flow_snmp.flow_data_local_new (pipe_id, time, in_flow, out_flow, in_bps, out_bps) VALUES"
client.execute(insert_sql, data_list)

