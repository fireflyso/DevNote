import requests
import json
from datetime import datetime, timedelta

count = 0
total_in = 0
total_out = 0
total_value = 0


def get_data(start_time, end_time):
    global count, total_in, total_out, total_value
    p = {
        "start_time": start_time,
        "end_time": end_time,
        "cloud_id": "a240bca6-ca7f-11eb-a6a9-421c197ea2ab"
    }
    try:
        res = requests.post("http://localhost:8081/bps_95/", json.dumps(p)).content
        data = json.loads(res)['data'][0]
        in_bps = data['in_bps']
        out_bps = data['out_bps']
        value = data['value']
        count += 1
        total_in += in_bps
        total_out += out_bps
        total_value += value
        print('{} - {} 的数据为：in_bps : {}, out_bps : {}, value : {}'.format(start_time, end_time, in_bps, out_bps, value))
    except Exception as e:
        print(e)
       

start_time = "2021-06-28 15:00:00"
end_time = "2021-06-28 23:59:59"
# end_time = "2021-07-23 16:00:00"
get_data(start_time, end_time)

for _ in range(24):
    start_time = end_time
    end_time = str(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(1))
    get_data(start_time, end_time)

start_time = "2021-07-23 00:00:00"
end_time = "2021-07-23 16:00:00"
get_data(start_time, end_time)
print("avg in : {}, out : {}, value : {}".format(
    round(total_in/count, 2),
    round(total_out/count, 2),
    round(total_value/count, 2)
))




