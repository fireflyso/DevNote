# coding=utf-8
# 操作线上库，慎用
import pymysql
import traceback

db = pymysql.connect(
    host="10.2.10.17",
    user="root",
    password="4CbPsJJo",
    database="cdscp_trunk",
    port=3306,
    charset='utf8'
)

cursor = db.cursor()
try:
    sql = "truncate table cloud_customer_conf_record;"
    cursor.execute(sql)
except:
    db.rollback()
    traceback.print_exc()
else:
    db.commit()
finally:
    cursor.close()
