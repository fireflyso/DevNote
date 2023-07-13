# -- coding: utf-8 --
# @Time : 2023/5/19 14:49
# @Author : xulu.liu

import requests
import json

api = "http://localhost/v1/resop/app/create/"
# 线上参数
data = {
    "user_id": "18600529015",
    "customer_id": "E036042",
    "app_name": "api create test99",
    "goods_id": 19316,
    "site_id": "1af1d06e-e2ad-41e7-97b0-ed77417fd3d4",
    "ip_num": 4,
    "is_auto_renewal": 0,
    "wan_name": "test wan",
    "qos": 5,
    "project_id": "f17696bc-fb47-11eb-9bf9-6e53a86a2e4f",
    "is_to_month": 0,
    "duration": 2,
    "preferential_coupon_id": "test",
}

res = requests.post(url=api, data=data)
json.loads(res.content.decode('utf8'))
