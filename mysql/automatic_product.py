# coding=utf-8
# 操作线上库，慎用
import pymysql
import traceback

# 打开数据库连接
db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="automatic_product",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()
try:
    # sql = "update route set route_name = 'DEFRA-FR7-ASR9K-GW-01' where route_id = '60f62cde-f606-4860-b433-13bd7f7961f5'"
    # cursor.execute(sql)
    # sql = "update route set route_name = 'DEFRA-FR7-ASR9K-GW-02' where route_id = '0b8d40ba-e41a-47f5-9478-cfbce3810af4'"
    sql = "update subinterface set interface_id = '3c12abf5-11ca-48d4-848a-5665d767d1c6' where subinterface_id = '0237d2b6-d3e5-4184-a7f4-7fd8ea986fe4'"
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    traceback.print_exc()
finally:
    cursor.close()
