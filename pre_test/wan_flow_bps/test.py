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

api = "http://localhost:9999/flow"
start_time = (datetime.now() - timedelta(days=1)).replace(microsecond=0)
mid_time = start_time + timedelta(hours=1)
end_time = start_time + timedelta(hours=2)
# 线上参数
data = {
    "start_time": str(start_time),
    "end_time": str(end_time),
    "cloud_id": 'd9641931-2ca3-4940-9100-b31f5459130a'
}

res = requests.post(url=api, data=data)
print(json.loads(res.content))