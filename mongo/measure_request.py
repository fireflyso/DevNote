import requests
import json
pipe_id = '003fd156-e258-11e8-baa8-0242ac110002'
p = {"start_time": "2021-04-01 00:00:00", "end_time": "2021-05-01 00:00:00", "cloud_id": pipe_id}
requests.post("http://10.13.2.235:6005/bps_95", json.dumps(p)).content


p = {"start_time": "2021-04-30 23:00:00", "end_time": "2021-05-01 00:00:00", "cloud_id": pipe_id}
requests.post("http://10.13.2.235:6005/bps_list", json.dumps(p)).content


p = {"start_time": "2021-04-30 00:00:00", "end_time": "2021-05-01 00:00:00", "cloud_id": pipe_id}
requests.post("http://10.13.2.235:6005/hour_bps_list", json.dumps(p)).content
