# coding=utf-8
import pymysql
import traceback

db = pymysql.connect(
    host="10.4.16.8",
    user="root",
    password="4CbPsJJo",
    database="cdscp",
    port=3307,
    charset='utf8'
)

cursor = db.cursor()
cursor.execute("select count(*) from pod;")
res = cursor.fetchall()
breakpoint()
# try:
#     sql = "truncate table cloud_customer_conf_record;"
#     cursor.execute(sql)
# except:
#     db.rollback()
#     traceback.print_exc()
# else:
#     db.commit()
# finally:
#     cursor.close()
