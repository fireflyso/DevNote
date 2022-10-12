import pymysql
from clickhouse_driver import Client
from datetime import datetime, timedelta
from utils_logger import get_logger
import requests
import json

logger = get_logger('unity_eip_flow_check', log_level='INFO')

percent = 0.8
start_time = datetime.now() - timedelta(minutes=20)
end_time = datetime.now() - timedelta(minutes=10)

def send_notification(content="大家好"):
    """
    异常消息通知
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3332e064-c96d-4bf9-8c2a-878b91c1b3b2"
    h = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    try:
        requests.post(url, headers=h, data=json.dumps(data))
    except Exception as e:
        logger.exception('告警信息发送失败 ： {}'.format(e))


db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

sql = "select a.id, a.qos, b.ip from cloud_os_bandwidth a, cloud_os_eip b where a.customer_id = 'C018455' and a.is_valid = 1 and a.id = b.bandwidth_id"
_ = cursor.execute(sql)
res = cursor.fetchall()
bandwidth_ids = []
qos_dict = {}
eip_dict = {}
for r in res:
    bandwidth_ids.append(r[0])
    qos_dict[r[0]] = r[1]
    eip_dict[r[0]] = r[2]

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

bandwidth_ids = tuple(bandwidth_ids)

start_time = str(start_time).split('.')[0]
end_time = str(end_time).split('.')[0]
logger.info("检测程序开始运行, 本次将检查的带宽资源数量为 : {}".format(len(bandwidth_ids)))
# 查询主表数据
master_sql = "select pipe_id, time, in_bps, out_bps from flow_snmp.flow_data where time >= '{}' and time < '{}' and pipe_id in {}".format(
    start_time, end_time, bandwidth_ids
)
master_res = client.execute(master_sql)
master_res = {'{}&{}'.format(m[0], m[1]): {'in_bps': m[2], 'out_bps': m[3]} for m in master_res}

# 查询附表数据
slave_sql = "select pipe_id, time, in_bps, out_bps from flow_snmp.flow_data_second_all where time >= '{}' and time < '{}' and pipe_id in {}".format(
    start_time, end_time, bandwidth_ids
)
slave_res = client.execute(slave_sql)
slave_res = {'{}&{}'.format(m[0], m[1]): {'in_bps': m[2], 'out_bps': m[3]} for m in slave_res}

mbps = 1024*1024
except_list = []

for k, v in master_res.items():
    pipe_id = k.split('&')[0]
    qos = qos_dict.get(pipe_id, 0)
    eip = eip_dict.get(pipe_id, '')
    if qos == 0 or eip == '':
        logger.error("{} 资源的带宽eip信息异常 ： {}, {}".format(pipe_id, qos, eip))
        continue

    slave_flow = slave_res.get(k, None)
    if not slave_flow:
        logger.error('{} 资源没有从设备的计量信息'.format(pipe_id))
        continue
    in_bps = v.get('in_bps') + slave_flow.get('in_bps')
    out_bps = v.get('out_bps') + slave_flow.get('out_bps')
    flow = in_bps if in_bps > out_bps else out_bps
    if flow/mbps >= qos * percent:
        logger.warn("带宽: {}, eip : {}， 时间节点 : {} 流量超限, 购买带宽为: {}, 入网带宽: {}, 出网带宽: {}".format(
            pipe_id, eip, k.split('&')[-1], qos, round(in_bps/mbps, 2), round(out_bps/mbps, 2)))
        except_list.append("eip: {}, {}, qos: {}, in: {}, out: {}".format(
            eip, k.split('&')[-1], qos, round(in_bps/mbps, 2), round(out_bps/mbps, 2)))

logger.info('带宽资源检测结束，收集到告警信息 {} 条，具体信息可以在warn日志文件中查看!'.format(len(except_list)))
if len(except_list) > 0:
    content = '当前超限阈值为 : {}, 以下资源流量超限 ! \n'.format(percent)
    for i in except_list:
        content += '{}\n'.format(i)
    send_notification(content)
