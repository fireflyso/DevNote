import requests
import json

pipe_id = '1edfb184-0a5f-11e8-9330-0242ac110002'
p = {"start_time": "2021-08-30 23:00:00", "end_time": "2021-10-01 00:00:00", "cloud_id": pipe_id}
requests.post("http://10.13.2.235:6005/avg_bps_95/", json.dumps(p)).content
