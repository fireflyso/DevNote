# -- coding: utf-8 --
# @Time : 2023/7/3 20:12
# @Author : xulu.liu

from clickhouse_driver import Client
CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_PORT = 9000
ck_client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
res = ck_client.execute("select distinct pipe_id from flow_snmp.flow_data where time >= '2023-07-03 00:00:00' and time < '2023-07-03 00:30:00'")
pipe_list = [r[0] for r in res]
total = len(pipe_list)
print('pipe count : {}'.format(total))
check = 0

fix_list = []
#ck_client.execute("select count(*) from system.mutations where is_done = 0;")

for pipe_id in pipe_list:
    check += 1
    res = ck_client.execute("select time, in_bps, out_bps from flow_snmp.flow_data where time >= '2023-07-03 06:00:00' and time < '2023-07-03 20:00:00' and pipe_id = '{}' order by time".format(pipe_id))
    if not res:
        continue
    start_time = res[0][0]
    temp_in = 0
    temp_out = 0
    count = 0
    max_value = 0
    stand = 1024 * 1024 * 10
    for r in res:
        flow_time, in_bps, out_bps = r[0], r[1], r[2]
        max_value = max_value if in_bps < max_value else in_bps
        max_value = max_value if out_bps < max_value else out_bps
        if temp_in == in_bps and temp_out == out_bps:
            count += 1
        else:
            if count > 24 and max_value > stand:
                if flow_time < start_time:
                    continue
                # print('{}/{}  pipe : {}, {} - {} in : {}, out : {}'.format(total, check, pipe_id, start_time, flow_time, temp_in, temp_out))
                fix_list.append((pipe_id, str(start_time), str(flow_time), temp_in, temp_out))
                sql = "ALTER TABLE flow_snmp.flow_data_local_new DELETE WHERE pipe_id = '{}' and time >= '{}' and time <= '{}';".format(pipe_id, str(start_time), str(flow_time))
                print(sql)
                ck_client.execute(sql)
                break
            count = 0
            start_time = flow_time
            temp_in = in_bps
            temp_out = out_bps
print('\n\n\n')
print(fix_list)
print('count : {}'.format(len(fix_list)))
