# -*- coding: utf-8 -*-
import requests
import json
pipe_id = '04b2506e-a3fe-11eb-b808-9602cbfa07f9'
p = {"start_time": "2021-07-25 09:40:00", "end_time": "2021-07-25 10:00:00", "cloud_id": pipe_id}
r = requests.post('http://10.13.2.235:6005/bps_list', json.dumps(p))
# r = requests.post('http://wan-flow-bps.capitalcloud.net/bps_95', p)

headers = {'Content-Type': 'application/json'}
p_json = json.dumps(p)
r = requests.post('http://wan-flow-bps.gic.pre/bps_95', data=p_json, headers=headers).content
print("json1 res : {}".format(r))

r = requests.post('http://wan-flow-bps.gic.pre/bps_95', json=p).content
print("json2 res : {}".format(r))

r = requests.post('http://wan-flow-bps.gic.pre/bps_95', data=p).content
requests.get('http://vm-status-set-service.capitalcloud.net/health/', data=p).content
requests.post('http://vm-status-set-service.capitalcloud.net/get_public_pipe_95/', data=p).content
requests.post('http://vm-status-set-service.capitalcloud.net/get_public_pipe_95/', data=json.dumps(p)).content
requests.post('http://vm-status-set-service/get_public_pipe_95', data=json.dumps(p)).content
print("dict res : {}".format(r))


# vm_status_set项目线上环境
import requests
import json
pipe_id = '04b2506e-a3fe-11eb-b808-9602cbfa07f9'
p = {
    "start_time": "2022-10-26 11:12:00",
    "cloud_id": "f2e808de-54db-11ed-9672-c2c4df2a325c",
    "end_time": "2022-10-26 14:40:00"
}
requests.post('http://vm-status-set-service.capitalcloud.net/get_public_pipe_95/', data=json.dumps(p)).content