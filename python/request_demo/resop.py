# -- coding: utf-8 --
import requests
import threading
import time
import json


class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        api = "http://localhost/v1/resop/pipe/ip_reserve_sync/"
        # api = "http://resop.gic.test/v1/resop/pipe/ip_reserve_sync/"
        # 测试环境参数
        # data = {
        #     "pipe_id": "79d34cf2-d847-11ed-90e4-ee837ea78432",
        #     "use_desc": "test_{}".format(self.name),
        #     "use_type": "vm",
        #     "num": 1000,
        #     "customer_id": "E020910",
        #     "user_id": "18633335555"
        # }
        # 线上参数
        data = {
            "pipe_id": "4d4f1be4-dd46-11ed-82e2-e2773052d764",
            "use_desc": "test_{}".format(self.name),
            "use_type": "vm",
            "num": 1,
            "customer_id": "E104616",
            "user_id": "630387"
        }
        start_t = time.time()
        res = requests.post(url=api, data=data)
        res_data = json.loads(res.content)
        if res_data['code_msg'] == 'success':
            ip_list = [r['ip'] for r in res_data['data'][:3]]
            print("{} - code_msg : {} , data len : {} , 耗时 : {}, ip list : {}".format(
                self.name, res_data['code_msg'], len(res_data['data']), time.time() - start_t, ip_list))
        else:
            print(res_data)


if __name__ == '__main__':
    thread_list = []
    for index in range(1):
        thread = MyThread("Thread-{}".format(index))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()
