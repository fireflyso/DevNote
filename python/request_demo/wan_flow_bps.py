import requests
api = "http://wan-flow-bps.gic.pre/bps_95/"
data = {'start_time': '2023-02-01 00:00:00', 'cloud_id': '1c79a138-7a33-11eb-97cf-eaa94a9340c5', 'end_time': '2023-03-01 00:00:00'}
res = requests.post(url=api, data=data)
print(res.content)


import requests
api = "http://localhost/slb_monitor_save"
data = {"active_conn": "IP Virtual Server version 0.0.0 |Prot LocalAddress:Port Scheduler Flags| -> RemoteAddress:Port Forward Weight ActiveConn InActConn|TCP 148.153.65.28:8080 conhash sip persistent 10| -> 10.241.94.1:80 FullNat 90 0 0 | -> 10.241.94.2:80 FullNat 99 0 0 |TCP 148.153.65.28:8088 rr persistent 10| -> 10.240.254.1:80 FullNat 0 0 0 | -> 10.240.254.2:80 FullNat 200 0 0 | -> 10.240.254.3:80 FullNat 100 0 0 |TCP 148.153.65.28:8888 rr persistent 10| -> 10.240.254.2:5201 FullNat 100 0 0 |", "all_conn": "IP Virtual Server version 0.0.0 |Prot LocalAddress:Port Conns InPkts OutPkts InBytes OutBytes| -> RemoteAddress:Port|TCP 148.153.65.28:8080 38 312 248 53770 24375| -> 10.241.94.1:80 2 8 7 558 623| -> 10.241.94.2:80 36 304 241 53212 23752|TCP 148.153.65.28:8088 0 0 0 0 0| -> 10.240.254.1:80 0 0 0 0 0| -> 10.240.254.2:80 0 0 0 0 0| -> 10.240.254.3:80 0 0 0 0 0|TCP 148.153.65.28:8888 12 1252024 302107 1853331013 12085248| -> 10.240.254.2:5201 12 1252024 302107 1853331013 12085248|", "slb_vm_id": "2775b8c4-dea4-11ed-848c-b221a761ce0e", "monitor_date": "2023-04-24 18:59:36"}
res = requests.post(url=api, data=data)
print(res.content)

import requests
url='http://localhost:80/bps_list'
data = {"start_time": "2023-04-23 11:10:00", "end_time": "2023-04-24 11:10:32", "cloud_id": "81039f60-dea3-11ed-b43e-d605018710e0"}
res = requests.post(url=url, data=data)
print(res.content)

res.status_code

