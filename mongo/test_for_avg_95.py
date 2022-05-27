import requests
import json

pipe_list = ['84e50556-0a2d-11e8-a293-0242ac110002']
for pipe_id in pipe_list:
    # 先调用老的95
    p = {
        "start_time": "2021-10-22 10:00:00",
        "end_time": "2021-11-22 11:00:00",
        "cloud_id": pipe_id
    }
    res = requests.post("http://10.13.2.235:6005/avg_bps_95/", json.dumps(p)).content
    print('--- pipe id : {} ---'.format(pipe_id))
    print("老接口数据 : {}".format(res))
    # 调用新的95
    res = requests.post("http://10.13.103.34/avg_bps_95/", json.dumps(p)).content
    print("新接口数据 : {}".format(res))