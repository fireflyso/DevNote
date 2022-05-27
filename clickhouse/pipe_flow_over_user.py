# coding=utf-8
# 操作线上库，慎用
import datetime
import time

import pymysql
import traceback

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

from clickhouse_driver import Client

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
FLOW_TABLE_NAME = "flow_data"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

sql = "SELECT p.id, p.qos from cloud_pipe p, cloud_gic_app_network n, cloud_gic g where p.id = n.pipe_id and n.gic_id = g.id and p.is_valid =1 and g.is_valid =1"
res = cursor.execute(sql)
res_list = cursor.fetchall()
pipe_ids = ["'{}'".format(pipe[0]) for pipe in res_list]
pipe_qos_dir = {pipe[0]: pipe[1] for pipe in res_list}

print('pipe count : {}'.format(len(pipe_ids)))
end_time = datetime.datetime.now()
interval = 60
start_time = (end_time - datetime.timedelta(minutes=interval)).strftime("%Y-%m-%d %H:%M:%S")
query = "SELECT pipe_id,time, in_bps, out_bps FROM {}.{} where pipe_id  in ({}) and time >= '{}'".format(
    CK_DB_ANME, FLOW_TABLE_NAME, ','.join(pipe_ids), start_time)

start_at = time.perf_counter()
res = client.execute(query)
print(len(res))
print('查询结束 用时 : {}'.format(time.perf_counter() - start_at))
pipe_flow_dir = {}
for r in res:
    pipe_id = r[0]
    pipe_flow = {
        'pipe_id': r[0],
        'time': r[1],
        'in_bps': r[2],
        'out_bps': r[3],
    }
    pipe_flow_dir.setdefault(pipe_id, []).append(pipe_flow)

warn_pipe_list = []
for pipe_id, pipe_flows in pipe_flow_dir.items():
    pipe_flows = sorted(pipe_flows, key=lambda e: e.__getitem__('time'), reverse=False)
    qos = pipe_qos_dir.get(pipe_id, 0) * 1024 * 1024

    over_count = 0
    total_count = len(pipe_flows)
    pipe_flow_count = len(pipe_flows)
    is_qos_over = False
    max_in_bps = 0
    max_out_bps = 0
    over_flow_list = []
    for index in range(pipe_flow_count - 1):
        if pipe_flows[index].get('in_bps') > qos or pipe_flows[index].get('out_bps') > qos:
            max_in_bps = pipe_flows[index].get('in_bps') if pipe_flows[index].get('in_bps') > max_in_bps else max_in_bps
            max_out_bps = pipe_flows[index].get('out_bps') if pipe_flows[index].get('out_bps') > max_out_bps else max_out_bps
            over_count += 1
            if not is_qos_over and index < pipe_flow_count - 1 and pipe_flows[index + 1].get('in_bps') > qos or pipe_flows[index + 1].get('out_bps') > qos:
                is_qos_over = True
                over_flow_list.append(pipe_flows[index])
                over_flow_list.append(pipe_flows[index + 1])

    if is_qos_over:
        warn_pipe_list.append(
            (pipe_id, pipe_qos_dir.get(pipe_id, 0), max_in_bps, max_out_bps, total_count, over_count, over_flow_list)
        )

if warn_pipe_list:
    subject = 'GNP流量超限预警'
    content = "{} - {} 以下GPN流量超限，请处理</br></br>".format(start_time, end_time.strftime("%Y-%m-%d %H:%M:%S"))
    for info in warn_pipe_list:
        pipe_id, qos, max_in_bps, max_out_bps, total_count, over_count, pipe_flows = info
        time_one = pipe_flows[0].get('time', '')
        out_bps_one = round(pipe_flows[0].get('out_bps', '') / 1024 / 1024, 2)
        in_bps_one = round(pipe_flows[0].get('in_bps', '') / 1024 / 1024, 2)
        time_two = pipe_flows[1].get('time', '')
        out_bps_two = round(pipe_flows[1].get('out_bps', '') / 1024 / 1024, 2)
        in_bps_two = round(pipe_flows[1].get('in_bps', '') / 1024 / 1024, 2)
        content += 'pipe id : {},     带宽 : {} </br>&nbsp;&nbsp;&nbsp;&nbsp;' \
                   ' 计量节点数：{}, 超限节点数： {}; </br>&nbsp;&nbsp;&nbsp;&nbsp; ' \
                   ' 最大出向带宽 {} M, 最大入向带宽 {} M; </br>&nbsp;&nbsp;&nbsp;&nbsp; ' \
                   ' 连续超限节点一 : {} 出 {} M, 入 {} M; </br>&nbsp;&nbsp;&nbsp;&nbsp; ' \
                   ' 连续超限节点二 : {} 出 {} M, 入 {} M;</br>'.format(
            pipe_id, qos, total_count, over_count, round(max_out_bps / 1024 / 1024, 2),
            round(max_in_bps / 1024 / 1024, 2), time_one, out_bps_one, in_bps_one, time_two, out_bps_two, in_bps_two)

print(content)
