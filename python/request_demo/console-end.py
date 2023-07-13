# -- coding: utf-8 --
import requests
import threading
import time
import json



def run():
    # api = "http://resop-service/v1/resop/pipe/ip_reserve/"
    # data = {"num": 1000, "use_desc": "test", "segment_id": "2a2b413c-d847-11ed-b381-1611cc702a93", "segments": [{"start_ip": "10.0.0.1", "end_ip": "10.0.3.232"}], "customer_id": "E036042", "user_id": "18600529015"}
    api = "http://localhost/v1/resop/pipe/ip_reserve_sync/"
    data = {
        "pipe_id": "2651bcc6-d847-11ed-a84e-ea9602e5cd4a",
        "use_desc": "test_{}",
        "use_type": "vm",
        "num": 1000,
        "customer_id": "E036042",
        "user_id": "18600529015"
    }
    start_t = time.time()
    res = requests.post(url=api, data=data)
    import pdb
    pdb.set_trace()
    res_data = json.loads(res.content)
    if res_data['code_msg'] == 'success':
        ip_list = [r['ip'] for r in res_data['data'][:3]]
        print("code_msg : {} , data len : {} , 耗时 : {}, ip list : {}".format(res_data['code_msg'], len(res_data['data']), time.time() - start_t, ip_list))
    else:
        print(res_data)


if __name__ == '__main__':
    run()