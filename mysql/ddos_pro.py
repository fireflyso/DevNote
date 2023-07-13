# coding=utf-8
# 操作线上库，慎用
import pymysql
import traceback

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="ddos_suspend_20210108",
    password="y6tqOxsTTPmVGDTnfAw@",
    database="cds_ddos",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()
sql = "INSERT INTO cds_ddos.sh_cu_task (ip, task_id, status) VALUES ('139.159.101.82', '2107882', 2);"
cursor.execute(sql)
db.commit()
cursor.close()

