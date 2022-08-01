# coding=utf-8
# 计费上线测试
import pymysql
import requests
import json


db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

diff_pipes = set()


def get_api(api, query):
    print("开始对比接口: {}, 开始时间: {}, 结束时间: {}".format(api, query.get('start_time'), query.get('end_time')))
    old_res = requests.post('http://10.13.2.235:6005/{}'.format(api), json.dumps(query))
    old_res = json.loads(old_res.content)
    old_data = old_res['data']
    new_res = requests.post('http://wan-flow-bps.gic.pre/{}'.format(api), query)
    new_res.status_code
    import pdb
    pdb.set_trace()
    new_res = json.loads(new_res.content)
    new_data = new_res['data']
    if old_data != new_data:
        print(" ########  ERROR pipe {} 新老接口 {} 数据存在差异请检查  #######".format(pipe_id, api))
        print("*** old res: {}".format(old_data))
        print("*** new res: {}".format(new_data))
        diff_pipes.add(pipe_id)


cursor = db.cursor()
try:
    sql = "SELECT id from cloud_pipe where is_valid = 1 and type='public' and qos = 10000 limit 50"
    cursor.execute(sql)
    res_list = cursor.fetchall()
except Exception as e:
    print(e)
finally:
    cursor.close()

for res in res_list:
    pipe_id = res[0]
    print("\n ---   compare flow for pipe : {}   ---".format(pipe_id))

    one_day = {"start_time": "2021-08-16 10:00:00", "end_time": "2021-08-17 10:00:00", "cloud_id": pipe_id}
    get_api('bps_95', one_day)
    get_api('flow', one_day)

    one_month = {"start_time": "2021-07-22 10:00:00", "end_time": "2021-08-27 10:00:00", "cloud_id": pipe_id}
    get_api('bps_95', one_month)
    get_api('flow', one_month)

print("接口数据存在差异的pipe : {}".format(diff_pipes))
