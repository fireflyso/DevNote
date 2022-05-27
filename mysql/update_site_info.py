# coding=utf-8
# 修复分离带宽带来的脏数据 2021年08月13日
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
try:
    sql = "SELECT id,name from cloud_datacenter where is_valid = 1"
    cursor.execute(sql)
    res_list = cursor.fetchall()
    print('len : {}'.format(len(res_list)))
    for res in res_list:
        id = res[0]
        name = res[1]
        print(u"update site set site_name = '{}' where site_id = '{}'".format(name, id))
except Exception as e:
    print(e)
finally:
    cursor.close()
