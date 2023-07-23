# -- coding: utf-8 --
# @Time : 2023/7/22 11:19
# @Author : xulu.liu
import xlwt
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
pipe_list = []
with open("temp.out") as file:
    for line in file:
        pipe_list.append(line.replace('\n', ''))

sql = "select id from cloud_pipe where type = 'public' and id in {};".format(tuple(pipe_list))
_ = cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    print(r[0])
cursor.close()
