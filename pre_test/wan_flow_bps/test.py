# -- coding: utf-8 --
# @Time : 2023/7/6 10:52
# @Author : xulu.liu
import requests
import json

api = "http://localhost:9999/flow_monitor"
# 线上参数
data = {
    "mail": "",
    "interval": 30
}

res = requests.post(url=api, data=data)
print(json.loads(res.content))


import requests
import json
from datetime import datetime, timedelta

api = "http://localhost/bps_95"
start_time = (datetime.now() - timedelta(days=1)).replace(microsecond=0)
mid_time = start_time + timedelta(hours=1)
end_time = start_time + timedelta(hours=2)
# 线上参数
data = {
    "start_time": '2022-06-01 00:00:00',
    "end_time": '2023-07-01 00:00:00',
    "cloud_id": '4eaf5570-f45d-11ed-bb3b-fac1491bd8ed'
}

res = requests.post(url=api, data=data)
print(json.loads(res.content))