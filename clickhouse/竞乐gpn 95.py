import json

import requests as requests
import pymysql

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

_ = cursor.execute("select id, gpn_name from cloud_gic where customer_id = 'C015445' and is_valid = 1;")
gpn_list = cursor.fetchall()
for gpn in gpn_list:
    gpn_id = gpn[0]
    gpn_name = gpn[1]
    _ = cursor.execute("select pipe_id from cloud_gic_app_network where gic_id = '{}' and is_valid = 1;".format(gpn_id))
    pipe_list = cursor.fetchall()
    max = 0
    for pipe in pipe_list:
        pipe_id = pipe[0]
        query = {"start_time": "2022-06-01 00:00:00", "end_time": "2022-07-01 00:00:00", "cloud_id": pipe_id}
        new_res = requests.post('http://wan-flow-bps.gic.pre/max', query)
        new_res = json.loads(new_res.content)
        out_bps_max = new_res['data'][0]['out_bps_max']
        in_bps_max = new_res['data'][0]['in_bps_max']
        pipe_max = out_bps_max if out_bps_max > in_bps_max else in_bps_max
        max = max if max > pipe_max else pipe_max

    print("gpn id : {}, name : {} 业务峰值 : {}M".format(gpn_id, gpn_name, round(max/1000/1000, 2)))



