from subprocess import Popen, PIPE, STDOUT
import redis
from datetime import datetime
import threading
from clickhouse_driver import Client
import json


def get_ch_client():
    CK_HOST = "10.2.10.30"
    CK_USER = "default"
    CK_PASSWORD = "cds-china"
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database='wan_fping')
    return client


def get_ip_list():
    r = redis.Redis(host='10.2.10.126', port=6379, decode_responses=True, password='000415')
    prefix_keys = r.hkeys('AS4812_prefixes_ips')
    temp_list = r.hmget('AS4812_prefixes_ips', prefix_keys)
    ip_list = []
    for temp in temp_list:
        if temp:
            ip_list += temp.split("&")
    return ip_list


def exe_command(command):
    """
    执行 shell 命令并实时打印输出
    :param command: shell 命令
    :return: process, exitcode
    """
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    res_list = []
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            res_list.append(line.decode().strip())
    process.wait()
    return res_list


class MyThread(threading.Thread):
    def __init__(self, name, ip_list):
        threading.Thread.__init__(self)
        self.name = name
        self.ip_list = ip_list

    def run(self):
        ping_time = datetime.now()
        cmd = "fping {} -r 1 -b 32 -e -a -C 3".format(" ".join(self.ip_list).strip())
        res = exe_command(cmd)
        timeout_list, delay_dict = self.format_data(res)
        data_list = []
        for k, v in delay_dict.items():
            delay_data = {
                'src_ip': '140.210.95.1',
                'dst_ip': k,
                'ping_time': ping_time,
                'delay': v,
                'country_code': 'CN',
                'operator_id': 1,
                'asn': 4812
            }
            data_list.append(delay_data)

        client = get_ch_client()
        insert_sql = f"insert into fping_data (src_ip, dst_ip, ping_time, delay, country_code, operator_id, asn) VALUES"
        client.execute(insert_sql, data_list)

        sort_data = sorted(data_list, key=lambda e: e.__getitem__('delay'), reverse=True)
        r = redis.Redis(host='10.2.10.126', port=6379, decode_responses=True, password='000415')
        pipeline = r.pipeline()
        count = int(len(sort_data) * 0.05)
        for data in sort_data[:count]:
            data['ping_time'] = str(data['ping_time'])[:19]
            pipeline.lpush('mtr_task', json.dumps(data))
        pipeline.execute()


    def format_data(self, res_list):
        ip_set = set(self.ip_list)
        res_set = set()
        timeout_list = []
        delay_dict = {}
        for msg in res_list:
            ip = msg.split(':')[0].strip()
            res_set.add(ip)
            delay_list = msg.split(':')[-1].strip().split(' ')
            if '-' in delay_list or 'ICMP' in delay_list:
                timeout_list.append(ip)
            else:
                try:
                    delay_list = [float(i) for i in delay_list]
                    delay_dict[ip] = round(sum(delay_list) / 3, 2)
                except Exception as e:
                    print("告警数据 : {}".format(delay_list))
        timeout_list += list(ip_set - res_set)

        return timeout_list, delay_dict


def fping(ip_list: list):
    step = 100
    task_list = [ip_list[i:i + step] for i in range(0, len(ip_list), step)]
    thread_list = []
    index = 0
    start_time = datetime.now()
    for ip_list in task_list:
        thread = MyThread("Thread-{}".format(index), ip_list)
        thread_list.append(thread)
        thread.start()
        index += 1

    print('共计开启 {} 个线程，耗时 {}s'.format(index + 1, (datetime.now() - start_time).seconds))
    for thread in thread_list:
        thread.join()

print('start fping')
start_time = datetime.now()
ip_list = get_ip_list()
fping(ip_list)
print('fping {} 个IP耗时 : {}'.format(len(ip_list), (datetime.now() - start_time).seconds))

