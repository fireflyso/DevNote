# -- coding: utf-8 --
# @Time : 2023/5/19 14:49
# @Author : xulu.liu

import requests
import json

api = "http://localhost:8888/api/resop/wan/create_pub/"
# 线上参数
data = {
    "app_id": "47948b86-92b5-4efc-837d-dbfed22a3b1e",
    "bill_method": "Bandwidth",
    "customer_id": "E036042",
    "float_qos": 5,
    "ip_num": 4,
    "is_auto_renewal": 1,
    "qos": 5,
    "type": "Bandwidth_Multi_ISP_BGP",
    "user_from": "cdsapi",
    "user_id": "18600529015"
}

res = requests.post(url=api, data=data)
json.loads(res.content.decode('utf8'))
