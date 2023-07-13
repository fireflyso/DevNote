# -- coding: utf-8 --
# @Time : 2023/6/27 15:40
# @Author : xulu.liu
import requests
import json

api = "https://open.feishu.cn/open-apis/bot/v2/hook/692da4b4-920d-4d96-82ab-0b403739bc0b"
headers = {'Content-Type': 'application/json;charset=utf-8'}
# 线上参数
data = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "项目更新通知",
                "content": [
                    [{
                        "tag": "text",
                        "text": "项目有更新"
                    }
                    ]
                ]
            }
        }
    }
}

res = requests.post(url=api, json=data, headers=headers)
print(res.status_code)
print(json.loads(res.content))
