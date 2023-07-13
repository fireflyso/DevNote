# -- coding: utf-8 --
# @Time : 2023/7/1 16:50
# @Author : xulu.liu
# 对指定的pipe资源，从服务器上读取流量信息，并更新到ck
from clickhouse_driver import Client
import time as tt
import utils_logger
logger = utils_logger.get_logger('update', 'INFO')

CK_HOST = "10.13.133.133"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
def get_data_list():
    flow_list = []
    for line in open("2001.out"):
        time_str = line.split('.csv')[0]
        flow_time = '{}-{}-{} {}:{}:00'.format(time_str[:4], time_str[4:6], time_str[6:8], time_str[9:11], time_str[12:14])
        out_bps = float(line.split(',')[-2])
        in_bps = float(line.split(',')[-1].replace('\n', ''))
        # logger.info('time : {}, in : {}, out : {}'.format(flow_time, in_bps, out_bps))
        flow_list.append((flow_time, in_bps, out_bps))
    return flow_list


pipe_id = 'f69a5bfa-f45c-11ed-a219-e24846a47d7c'
flow_list = get_data_list()
count = 0
index = 0
total_count = len(flow_list)
for flow_data in flow_list:
    time, in_bps, out_bps = flow_data
    sql = "ALTER TABLE flow_snmp.flow_data_local_new UPDATE in_bps = {},out_bps = {} WHERE pipe_id = '{}' and time = '{}';".format(in_bps, out_bps, pipe_id, time)
    # logger.info(sql)
    client.execute(sql)
    index += 1
    count += 1
    if count >= 100:
        logger.info('进度 : {}/{}'.format(index, total_count))
        while count > 0:
            res = client.execute("select count(*) from system.mutations where is_done = 0;")
            if res[0][0] > 0:
                tt.sleep(10)
            else:
                count = 0
