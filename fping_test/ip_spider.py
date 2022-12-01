#!/usr/bin/python3
import subprocess
import redis
import threading
from multiprocessing import Process, Queue
from datetime import datetime


def subprocess_popen(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        re = p.stdout.readlines()  # 获取原始执行结果
        result = []
        for i in range(2, len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
            res = re[i].decode('utf-8').strip('\r\n')
            if "???" not in res:
                result.append(res.strip())
        return result


def ip_vote(ip_list: list, ip_count: int = 10) -> list:
    """
    从抓取到的IP列表中选出10个IP代表这个prefixes
    选取策略：尽量保证从不同的c段中选取，
    :param ip_list:
    :param ip_count: 指定需要从全量IP中挑选出多少个IP作为prefixes代表，默认10个
    :return: 挑选出来的IP列表
    """
    if type(ip_list) != list:
        print('参数类型异常 {}!'.format(type(ip_list)))
        return []

    if len(ip_list) <= ip_count:
        return ip_list

    # 进行IP挑选
    # 1.排除 x.x.x.0和x.x.x.255
    # 2.将IP按c段分组，轮询从每个网段中取数据直到取到10个IP为止
    # demo: ip_list = ['43.247.100.255', '43.247.100.114'...]
    ip_list = [ip for ip in ip_list if ip.split('.')[-1] not in ['0', '255']]
    # segment_dict = {
    #     '100': ['43.247.100.114', '43.247.100.120', '43.247.100.192', '43.247.100.193', '43.247.100.226'],
    #     ...
    # }
    segment_dict = {}
    for ip in ip_list:
        segment_dict.setdefault(ip.split('.')[-2], []).append(ip)

    segment_list = [v for k, v in segment_dict.items()]
    data_list = []
    # 这里用while写出来会更简洁，但是会出现死循环的风险
    for i in range(ip_count):
        if len(data_list) >= ip_count:
            break
        for ips in segment_list:
            if len(ips) >= i + 1:
                data_list.append(ips[i])
                if len(data_list) >= ip_count:
                    break

    return data_list


class MyThread(threading.Thread):
    def __init__(self, name, task_queue, start_time, res_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.task_queue = task_queue
        self.res_queue = res_queue
        self.start_time = start_time
        self.cmd = "fping -ag {} 2>/dev/null"

    def run(self):
        # print("开始线程：" + self.name)
        while not self.task_queue.empty():
            try:
                prefix = self.task_queue.get(timeout=3)
            except Exception as e:
                print('{} 获取任务失败，将再次尝试!'.format(self.name))
                continue

            try:
                ip_list = subprocess_popen(self.cmd.format(prefix))
                print("prefixes : {}, ips : {}".format(prefix, ip_list))
                ip_list = ip_vote(ip_list)
                data = (prefix, "&".join(ip_list))
                self.res_queue.put(data)
            except Exception as e:
                print(e)

        print('{}: 完成任务，即将关闭！'.format(self.name))


def get_prefixes_from_redis():
    r = redis.Redis(host='10.2.10.126', port=6379, decode_responses=True, password='000415')
    prefixes_count = r.llen('prefix_list')
    index = 0
    prefixes_list = []
    while index < prefixes_count:
        prefixes_list += r.lrange('prefix_list', index, index + 1000)
        index += 1000

    return prefixes_list


def send_ip_info(res_queue):
    r = redis.Redis(host='10.2.10.126', port=6379, decode_responses=True, password='000415')
    while not res_queue.empty():
        data = res_queue.get()
        r.hset('AS4812_prefixes_ips', data[0], data[1])


# 存放prefixes信息，理论上一个运营商的prefixes数量为500
start_time = datetime.now()
task_queue = Queue(10000)
res_queue = Queue(10000)
prefixes_list = get_prefixes_from_redis()
for prefixes in prefixes_list:
    task_queue.put(prefixes)
print('任务总数 : {}'.format(task_queue.qsize()))
thread_list = []
thread_count = 100
for c in range(thread_count):
    thread = MyThread("Thread-{}".format(c), task_queue, start_time, res_queue)
    thread_list.append(thread)
    thread.start()

print('共计开启 {} 个线程，耗时 {}s'.format(thread_count, (datetime.now() - start_time).seconds))
for thread in thread_list:
    thread.join()

send_ip_info(res_queue)
print("退出主线程, 总耗时 : {}s".format((datetime.now() - start_time).seconds))
