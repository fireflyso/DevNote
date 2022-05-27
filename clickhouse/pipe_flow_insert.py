'''
2021年11月9日 两个pipe的数据没有入库，需要从文件中读取计量信息手动入库
'''
import os
import csv
import time
from clickhouse_driver import Client
from datetime import datetime, timedelta

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"

CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
FLOW_TABLE_NAME = "flow_data_local_new"


def time_bulk_insert_db(data):
    try:
        data_list = [[
            v.get("pipe_id"),
            v.get("time"),
            v.get("in_flow"),
            v.get("out_flow"),
            v.get("in_bps"),
            v.get("out_bps"),
        ] for v in data]
        if data_list:
            client = Client(host=CK_HOST, port=CK_PORT, database=CK_DB_ANME, user=CK_USER, password=CK_PASSWORD)
            insert_sql = f"insert into {CK_DB_ANME}.{FLOW_TABLE_NAME} (pipe_id, time, in_flow, out_flow, in_bps, out_bps) VALUES"
            client.execute(insert_sql, data_list)
            client.disconnect()
    except Exception as e:
        print(e)
        return False
    return True

folder_list = [
    '20211029',
    '20211030',
    '20211031',
    '20211101',
    '20211102',
    '20211103',
    '20211104',
    '20211105',
    '20211106',
    '20211107',
    '20211108',
    '20211109'
]
base_path = '/home/snmp_data/139.159.48.253/flow/flow_rsync/'
for folder in folder_list:
    bps_list = []
    folder_path = base_path + folder
    all_file_list = os.listdir(folder_path)
    all_file_list.sort()
    for file_name in all_file_list:
        if file_name.split('.')[-1] == 'csv':
            csv_file_path = '{}/{}'.format(folder_path, file_name)
            with open(csv_file_path) as f:
                f_csv = csv.reader(f)
                headers = next(f_csv)
                flow_data = list(f_csv)

            for line in flow_data:
                if line[0] == 'Bundle-Ether8.2782':
                    pipe_id = '53d224fa-3de4-11ec-bf67-eeb3ef90bb34'
                elif line[0] == 'Bundle-Ether8.2106':
                    pipe_id = '91d5cc3c-37b5-11ec-9fe1-66a49d288429'
                else:
                    continue

                stamp = int(line[1])
                time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(stamp)))
                tmp = {
                    "pipe_id": pipe_id,
                    "time": datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S'),
                    "in_flow": float(line[3]),
                    "out_flow": float(line[2]),
                    "in_bps": float(line[5]),
                    "out_bps": float(line[4]),
                }
                if stamp < 1636448651:
                    bps_list.append(tmp)

    time_bulk_insert_db(bps_list)
    print('{}成功插入 {} 条数据'.format(folder, len(bps_list)))



