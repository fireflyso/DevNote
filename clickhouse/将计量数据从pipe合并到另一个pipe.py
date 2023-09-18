from clickhouse_driver import Client

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

start_time = '2023-08-01 00:00:00'
end_time = '2023-08-30 00:00:00'

src_pipe_id = '517bb94e-3d8b-11ed-8622-62779b56db9a'
dst_pipe_id = 'e98620fe-3a78-11ee-aad7-c2488d702a72'

src_res = client.execute("SELECT time, in_flow, out_flow, in_bps, out_bps FROM flow_snmp.flow_data where "
                         "pipe_id  = '{}' and time >= '{}' and time < '{}' order by time".format(
                            src_pipe_id, start_time, end_time))
dst_res = client.execute("SELECT time, in_flow, out_flow, in_bps, out_bps FROM flow_snmp.flow_data where "
                         "pipe_id  = '{}' and time >= '{}' and time < '{}' order by time".format(
                            dst_pipe_id, start_time, end_time))
dst_dict = {d[0]: d for d in dst_res}

src_insert_list = []
dst_insert_list = []
for src_data in src_res:
    time_str = src_data[0]
    src_insert_list.append({
        'pipe_id': src_pipe_id,
        'time': time_str,
        'in_flow': src_data[1],
        'out_flow': src_data[2],
        'in_bps': 0,
        'out_bps': 0
    })
    dst_data = dst_dict.get(time_str, ())
    if not dst_data:
        # print('------ {} 节点数据不齐'.format(src_data))
        dst_insert_list.append({
            'pipe_id': dst_pipe_id,
            'time': time_str,
            'in_flow': 0,
            'out_flow': 0,
            'in_bps': src_data[3],
            'out_bps': src_data[4]
        })
        continue
    # print('{} - src pipe flow : {}, {}'.format(time_str, src_data[3], src_data[4]))
    # print('{} - dst pipe flow : {}, {}'.format(time_str, dst_data[3], dst_data[4]))
    dst_insert_list.append({
        'pipe_id': dst_pipe_id,
        'time': time_str,
        'in_flow': dst_data[1],
        'out_flow': dst_data[2],
        'in_bps': src_data[3] + dst_data[3],
        'out_bps': src_data[4] + dst_data[4]
    })


ck_sql = "Alter table flow_snmp.flow_data_local_new DELETE where pipe_id = '{}' and time >= '{}' and time < '{}'".format(
    dst_pipe_id, start_time, end_time)
client.execute(ck_sql)

ck_sql = "Alter table flow_snmp.flow_data_local_new DELETE where pipe_id = '{}' and time >= '{}' and time < '{}'".format(
    src_pipe_id, start_time, end_time)
client.execute(ck_sql)

insert_sql = f"insert into flow_snmp.flow_data_local_new (pipe_id, time, in_flow, out_flow, in_bps, out_bps) VALUES"
client.execute(insert_sql, src_insert_list)
client.execute(insert_sql, dst_insert_list)
