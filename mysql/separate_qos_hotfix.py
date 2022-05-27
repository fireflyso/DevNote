# coding=utf-8
# 修复分离带宽带来的脏数据 2021年08月13日
import pymysql
import requests
import time

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()
try:
    sql = "SELECT p.id, p.cds_resource_id, p.app_id, p.qos, e.real_qos, e.in_qos, e.out_qos from cloud_pipe_extend e, cloud_pipe p where e.pipe_id = p.id and e.out_qos > p.qos and e.pipe_id not in ('197eecd6-fb48-11eb-844a-120c1bbf1f19', '34822954-fb51-11eb-844a-120c1bbf1f19', 'ac0f372e-d7dd-11eb-83d1-cefefb406359', '6d7d7e46-f103-11eb-bdd6-7e39ccda27b2', '5319ea1a-fb50-11eb-b125-4277d6c84d6d', 'c2819240-eba1-11eb-a6ff-46ab5ca77e96', '6f8cb5a2-ef79-11eb-a837-eae02e143911', '55a32636-b305-11eb-9fd1-cebea080f1a0', '6047b68a-af16-11eb-94af-0242ac110a60', '1bf00e40-f405-11eb-9ce4-66b166fc6a03')"
    cursor.execute(sql)
    res_list = cursor.fetchall()
    for res in res_list:
        params = {
            'subinterface_id': res[1],
            'pipe_id': res[0],
            'app_id': res[2],
            'in_qos': res[3],
            'out_qos': res[3]
        }
        url = 'http://10.13.2.235:7505/api/pipe/separate_qos'
        api_res = requests.post(url, params)
        print("pipe : {} 任务下发结果 : {}".format(res[0], api_res.content))
        time.sleep(1)

except Exception as e:
    print(e)
finally:
    cursor.close()
