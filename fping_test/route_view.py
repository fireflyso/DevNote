from clickhouse_driver import Client
import json
from datetime import datetime, timedelta


def get_ch_client():
    CK_HOST = "10.2.10.30"
    CK_USER = "default"
    CK_PASSWORD = "cds-china"
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database='wan_fping')
    return client


ip = '180.167.3.12'
client = get_ch_client()
sql = "select * from wan_fping.mtr_route where dst_ip = toIPv4('{}') order by update_time desc limit 1;".format(ip)
res_list = client.execute(sql)
for res in res_list:
    mtr_time = res[2]
    print('time : {} 地址 ：{} --> {}'.format(mtr_time, str(res[0]), str(res[1])))
    route_list = json.loads(res[3])
    for index in range(len(route_list)-1):
        src_ip = route_list[index][0]
        dst_ip = route_list[index + 1][0]
        delay = route_list[index + 1][1]
        sql = "select count(*), avg(delay) from wan_fping.mtr_time where '{}' >= mtr_time and mtr_time.mtr_time >= '{}' and src_ip = toIPv4('{}') and dst_ip = toIPv4('{}');".format(
            mtr_time + timedelta(minutes=5), mtr_time - timedelta(minutes=5), src_ip, dst_ip)
        data_info = client.execute(sql)[0]
        print("步骤 {} : {} --> {} 延时 : {}, 全库同时段有 {} 次该路径统计, 平均延时为 : {}".format(
            index+1, src_ip, dst_ip, delay, data_info[0], round(data_info[1], 2)))
