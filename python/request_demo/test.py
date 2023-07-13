# -- coding: utf-8 --
import requests
import json

api = "http://localhost/v2/resop/vm/reverse_ip/"
# 线上参数
data = {
    "pipe_id": "2651bcc6-d847-11ed-a84e-ea9602e5cd4a",
    "desc": "lxl",
    "used_type": "vm",
    "address_list": [],
    "reverse_type": "auto",
    "reverser_num": 3,
    "customer_id": "E036042",
    "user_id": "18600529015"
}

res = requests.post(url=api, data=data)
json.loads(res.content)


import requests
import json

api = "http://localhost/v1/resop/pipe/ip_reserve_sync/"
# 线上参数
data = {
    "pipe_id": "2651bcc6-d847-11ed-a84e-ea9602e5cd4a",
    "use_desc": "test_lxl",
    "use_type": "vm",
    "num": 5,
    "customer_id": "E036042",
    "user_id": "18600529015"
}

res = requests.post(url=api, data=data)
json.loads(res.content)
