"""
美图数据修复
- 美图共享带宽：20929d02-5a1d-11ee-bb54-4e35d34f6fb5 从2023-09-29 16:15:00 开始丢失计量数据
- 数据迁移到共享带宽：1f318dca-5eb3-11ee-94e1-660920dc2c55 上，从2023-09-29 19:00:00开始有计量数据
"""
from clickhouse_driver import Client

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
FLOW_TABLE_NAME = 'flow_data_local_new'

start_time = '2023-10-18 20:15:00'

test_pipe_id = '1f318dca-5eb3-11ee-94e1-660920dc2c55'
meitu_pipe_id = '20929d02-5a1d-11ee-bb54-4e35d34f6fb5'


def clear_history():
    ck_sql = "Alter table flow_snmp.flow_data_local_new DELETE where pipe_id = '{}' and time >= '{}'".format(
        meitu_pipe_id, start_time)
    client.execute(ck_sql)


def insert_new():
    test_flow_list = client.execute(
        "select time, in_bps, out_bps from flow_snmp.flow_data_local_new where pipe_id = '{}' and time >= '{}' "
        "order by time".format(test_pipe_id, start_time))
    ck_data_list = []
    for flow_data in test_flow_list:
        flow_time, in_bps, out_bps = flow_data
        ck_data_list.append([meitu_pipe_id, flow_time, in_bps, out_bps])

    insert_sql = f"insert into {CK_DB_ANME}.{FLOW_TABLE_NAME} (pipe_id, time, in_bps, out_bps) VALUES"
    client.execute(insert_sql, ck_data_list)


if __name__ == '__main__':
    clear_history()
    insert_new()
