"""
美图数据修复
- 美图共享带宽：20929d02-5a1d-11ee-bb54-4e35d34f6fb5 从2023-09-29 16:15:00 开始丢失计量数据
- 数据迁移到共享带宽：1f318dca-5eb3-11ee-94e1-660920dc2c55 上，从2023-09-29 19:00:00开始有计量数据
"""
from clickhouse_driver import Client
from datetime import datetime, timedelta

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
FLOW_TABLE_NAME = 'flow_data_local_new'

test_pipe_id = '1f318dca-5eb3-11ee-94e1-660920dc2c55'
meitu_pipe_id = '20929d02-5a1d-11ee-bb54-4e35d34f6fb5'


def update_flow(test_flow_list):
    print(test_flow_list)
    for flow_data in test_flow_list:
        flow_time, in_bps, out_bps = flow_data
        sql = "ALTER TABLE flow_snmp.flow_data_local_new UPDATE in_bps = {},out_bps = {} WHERE pipe_id = '{}' " \
              "and time = '{}';".format(in_bps, out_bps, meitu_pipe_id, flow_time)
        client.execute(sql)


def get_last_flow():
    last_20 = str((datetime.now() - timedelta(minutes=20)).replace(microsecond=0))
    test_flow_list = client.execute(
        "select time, in_bps, out_bps from flow_snmp.flow_data_local_new where pipe_id = '{}' and time >= '{}' "
        "order by time".format(test_pipe_id, last_20))
    if not test_flow_list:
        raise '{} 最新流量节点获取失败！'.format(test_pipe_id)
    return test_flow_list


if __name__ == '__main__':
    print('start : {} ---'.format(datetime.now()))
    test_flow_list = get_last_flow()
    update_flow(test_flow_list)
    client.disconnect()
    print('end : {} ---\n'.format(datetime.now()))

