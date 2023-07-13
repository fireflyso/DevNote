# -- coding: utf-8 --
# @Time : 2023/4/26 14:45
# @Author : xulu.liu
import requests

api = "http://ddos-suspend.gic.pre/api/v1/sh_cu/get_sh_cu_task_id/"
data = {"ip": "127.0.0.1"}
res = requests.post(url=api, data=data)
print(res.content)


api = "http://localhost:6009/api/v1/sh_cu/get_sh_cu_unban_task_id/"
data = {"ip": "127.0.0.1"}
res = requests.post(url=api, data=data)
print(res.content)

import requests
api = "http://localhost:6009/api/v1/sh_cu/get_sh_cu_ban_task_id/"
data = {"ip": "139.159.101.82"}
res = requests.post(url=api, data=data)
print(res.content)

import requests
api = "http://localhost:6009/api/v1/sh_cu/add_sh_cu_task/"
data = {
    "ip": "127.0.0.6",
    "task_id": "2097362",
    "status": 2
}
res = requests.post(url=api, data=data)
print(res.content)


import requests
api = "http://localhost:6009/api/v1/sh_cu/get_task_list/"
res = requests.post(url=api)
print(res.content)

import requests
api = "http://localhost:6009/api/v1/sh_cu/update_task_status/"
data = {
    "task_id": "2107882",
    "status": 6
}
res = requests.post(url=api, data=data)
print(res.content)
