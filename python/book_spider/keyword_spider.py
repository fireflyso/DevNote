import requests

url = 'http://wan-flow-bps-service/avg_bps_95'
data = {
    "start_time": "2021-12-01 00:00:00",
    "cloud_id": "35631dca-300f-11e9-8d22-0242ac110002",
    "end_time": "2022-01-01 00:00:00"
}

print(requests.post(url, data).content)