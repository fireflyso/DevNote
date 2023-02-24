import json
import requests
# SAVE_FPING_API = "http://127.0.0.1/api/product_info/"
SAVE_FPING_API = "http://wan-status-analysis.capitalonline.net/api/product_info/"
SAVE_FPING_API = "http://164.52.33.109:30110/api/product_info/"
data_list = {"product_id": 10}
res = requests.post(url=SAVE_FPING_API, json=data_list)
print(res.content)
