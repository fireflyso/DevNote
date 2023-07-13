import requests
api = "http://localhost:8888/api/slb_monitor/concurrent_conn/"
data = {"listen_id":"aa0b3950-d79a-11ed-9d4c-52456c0afbf3","start_time":"2023-04-10 20:24:39","end_time":"2023-04-11 12:30:10"}
res = requests.post(url=api, data=data)
print(res.content)
