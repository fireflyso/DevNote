import requests
import json

api = "http://localhost/api/v2/eip/create/"
# 线上参数-固定带宽
# data = {
#     "region_id": "cdc9be22-a6f8-11eb-be28-ca1003d55bcc",
#     "available_zone_id": "e5aa47be-da46-11ec-bad2-defff767b3b5",
#     "bandwidth_conf_id": 11950,
#     "bandwidth_billing_scheme_id": "283d7220-1dfb-11ed-a821-226ea6921122",
#     "qos": 10,
#     "size": 1,
#     "description": "",
#     "duration": 0,
#     "is_to_month": 1,
#     "user_id": "18600529015",
#     "customer_id": "E036042",
#     "preferential_coupon_id": "test"
# }
# 线上参数-固定带宽（包月）
data = {
    "region_id": "cdc9be22-a6f8-11eb-be28-ca1003d55bcc",
    "available_zone_id": "e5aa47be-da46-11ec-bad2-defff767b3b5",
    "bandwidth_conf_id": 11950,
    "bandwidth_billing_scheme_id": "56da6cd2-1dfb-11ed-887b-caeed1f5272c",
    "qos": 20,
    "size": 1,
    "description": "",
    "duration": 2,
    "is_to_month": 0,
    "is_auto_renewal": False,
    "user_id": "18600529015",
    "customer_id": "E036042",
    "preferential_coupon_id": "test11"
}

res = requests.post(url=api, data=data)
json.loads(res.content.decode('utf8'))


