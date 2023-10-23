"""
美图数据修复
- 美图共享带宽：20929d02-5a1d-11ee-bb54-4e35d34f6fb5 从2023-09-29 16:15:00 开始丢失计量数据
- 数据迁移到共享带宽：1f318dca-5eb3-11ee-94e1-660920dc2c55 上，从2023-09-29 19:00:00开始有计量数据
"""
from clickhouse_driver import Client
from datetime import datetime, timedelta
import json

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
FLOW_TABLE_NAME = 'flow_data_local_new'

test_pipe_id = '1f318dca-5eb3-11ee-94e1-660920dc2c55'
meitu_pipe_id = '20929d02-5a1d-11ee-bb54-4e35d34f6fb5'


def update_flow(first_flow_list, second_flow_list):
    print("first list: {}".format(first_flow_list))
    print("second list: {}".format(second_flow_list))
    for flow_data in first_flow_list:
        flow_time, in_bps, out_bps = flow_data
        sql = "ALTER TABLE flow_snmp.flow_data_local_new UPDATE in_bps = {},out_bps = {} WHERE pipe_id = '{}' " \
              "and time = '{}';".format(in_bps, out_bps, meitu_pipe_id, flow_time)
        client.execute(sql)
    for flow_data in second_flow_list:
        flow_time, in_bps, out_bps = flow_data
        sql = "ALTER TABLE flow_snmp.flow_data_second_local UPDATE in_bps = {},out_bps = {} WHERE pipe_id = '{}' " \
              "and time = '{}';".format(in_bps, out_bps, meitu_pipe_id, flow_time)
        client.execute(sql)


def get_last_flow(first_time, second_time):
    first_test_list = client.execute(
        "select time, in_bps, out_bps from flow_snmp.flow_data_local_new where pipe_id = '{}' and time > '{}' "
        "order by time".format(test_pipe_id, first_time))
    first_dic = {r['time']: r for r in first_test_list}
    second_test_list = client.execute(
        "select time, in_bps, out_bps from flow_snmp.flow_data_second_local where pipe_id = '{}' and time > '{}' "
        "order by time".format(test_pipe_id, second_time))
    second_dic = {r['time']: r for r in second_test_list}

    first_meitu_list = client.execute(
        "select time, in_bps, out_bps from flow_snmp.flow_data_local_new where pipe_id = '{}' and time > '{}' "
        "order by time".format(meitu_pipe_id, first_time))
    second_meitu_list = client.execute(
        "select time, in_bps, out_bps from flow_snmp.flow_data_second_local where pipe_id = '{}' and time > '{}' "
        "order by time".format(meitu_pipe_id, second_time))
    first_list = []
    for meitu in first_meitu_list:
        temp_time = meitu[0]
        flow_data = first_dic.get(temp_time, {})
        in_bps = meitu[1] + flow_data[1]
        out_bps = meitu[2] + flow_data[2]
        first_list.append((temp_time, in_bps, out_bps))
        first_time = temp_time

    second_list = []
    for meitu in second_meitu_list:
        temp_time = meitu[0]
        flow_data = second_dic.get(temp_time, {})
        in_bps = meitu[1] + flow_data[1]
        out_bps = meitu[2] + flow_data[2]
        second_list.append((temp_time, in_bps, out_bps))
        second_time = temp_time

    return first_list, second_list, first_time, second_time

def get_start_time():
    time = ''
    with open('time.out', 'r') as f:
        time = f.read()
    time = json.loads(time)
    return time[0], time[1]


def set_start_time(first_time, second_time):
    st = (first_time, second_time)
    print(st)
    a = open('time.out', 'w')
    a.write(json.dumps(st))
    a.close()


if __name__ == '__main__':
    first_time, second_time = get_start_time()
    print('start : {} ---'.format(datetime.now()))
    first_list, second_list, first_time, second_time = get_last_flow(first_time, second_time)
    update_flow(first_list, second_list)
    client.disconnect()
    print('end : {} ---\n'.format(datetime.now()))
    set_start_time(first_time, second_time)

