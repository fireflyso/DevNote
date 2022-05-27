import requests
import json
p = {
    "start_time": "2021-06-30 12:30:00",
    "end_time": "2021-07-30 12:30:00",
    "cloud_id": "6c6d7e6a-2375-11e9-9cc0-0242ac110002",
    "from_vpc": 1
}
requests.post("http://wan-flow-bps.capitalcloud.net/bps_95/", json.dumps(p)).content

pipe_id = '4fcefafa-76ee-11e9-811d-0242ac110002'
p = {"start_time": "2021-07-23 15:00:00", "end_time": "2021-07-23 16:00:00", "cloud_id": pipe_id}
requests.post("http://10.13.2.235:6005/bps_95", json.dumps(p)).content


p = {"start_time": "2021-04-30 23:00:00", "end_time": "2021-05-01 00:00:00", "cloud_id": pipe_id}
requests.post("http://10.13.2.235:6005/bps_list", json.dumps(p)).content


p = {'start_time': '2021-10-31 11:00:00', 'cloud_id': '35572c14-3894-11ec-8e29-ba6016034d9c', 'end_time': '2021-10-31 12:00:00'}
requests.post("http://10.13.2.235:6005/hour_bps_list", json.dumps(p)).content

