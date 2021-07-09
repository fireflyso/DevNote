# coding=utf-8
# 操作线上库，慎用
import pymysql
import traceback

# 打开数据库连接
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
    # sql = "DELETE from snmp_customer_flow_analysis where record_date = '2021-07-03 00:00:00'"
    sql = "update subinterface set interface_id = '3c12abf5-11ca-48d4-848a-5665d767d1c6' where subinterface_id = '0237d2b6-d3e5-4184-a7f4-7fd8ea986fe4'"
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    traceback.print_exc()
finally:
    cursor.close()
