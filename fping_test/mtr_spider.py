#!/usr/bin/python3
import redis
import threading
from datetime import datetime
import subprocess
import time
import json
import re
from clickhouse_driver import Client


def get_ch_client():
    CK_HOST = "10.2.10.30"
    CK_USER = "default"
    CK_PASSWORD = "cds-china"
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database='wan_fping')
    return client


def subprocess_popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while p.poll() is None:
        if p.wait() != 0:
            print("命令执行失败，请检查设备连接状态")
            return False
        else:
            re_data = p.stdout.readlines()
            result = []
            re_str = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
            for i in range(2, len(re_data)):
                res = re_data[i].decode('utf-8').strip('\r\n')
                if "???" not in res:
                    ip = res.strip().split(' ')[1]
                    delay = res.strip().split(' ')[-4]
                    if re.match(re_str, ip) and delay:
                        result.append((ip, float(delay)))
            return result


def save_to_clickhouse(client, data_list, src_ip, dst_ip):
    mtr_time = datetime.now()
    insert_sql = f"insert into mtr_route (src_ip, dst_ip, update_time, route) VALUES"
    client.execute(insert_sql, [{
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'update_time': mtr_time,
        'route': json.dumps(data_list)
    }])
    insert_data = []
    for index in range(len(data_list)-1):
        insert_data.append({
            'src_ip': data_list[index][0],
            'dst_ip': data_list[index + 1][0],
            'mtr_time': mtr_time,
            'delay': data_list[index][1],
        })

    insert_sql = f"insert into mtr_time (src_ip, dst_ip, mtr_time, delay) VALUES"
    client.execute(insert_sql, insert_data)


class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        # 消费的任务数量
        self.score = 0

    def run(self):
        r = redis.Redis(host='10.2.10.126', port=6379, decode_responses=True, password='000415')
        client = get_ch_client()
        while True:
            if r.llen('mtr_task') > 0:
                data = r.rpop('mtr_task')
                data = json.loads(data)
                print('{} : 开始处理任务 : {}'.format(self.name, data))
                cmd = "mtr -c 1 -rn {}".format(data.get('dst_ip'))
                result = subprocess_popen(cmd)
                print('{} : mtr结果 : {}'.format(data.get('dst_ip'), result))
                save_to_clickhouse(client, result, data.get('src_ip'), data.get('dst_ip'))
            else:
                time.sleep(3)

        print('线程 {} 完成任务，即将关闭！'.format(self.name))

    # 既可以判断执行是否成功，还可以获取执行结果


thread_list = []
thread_count = 10
for c in range(thread_count):
    thread = MyThread("Thread-{}".format(c))
    thread_list.append(thread)
    thread.start()

for thread in thread_list:
    thread.join()
