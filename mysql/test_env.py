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
    sql = "INSERT INTO `automatic_product`.`interface`(`interface_id`, `interface_name`, `pod_id`, `route_id`, `is_valid`) VALUES ('78fd154a-8d77-4882-8987-bf38e4c2324a', 'if_one', 'f4e072df-a165-4620-af2c-c2b4a570a107', '164a6d62-7320-49b3-84c6-ccb7f38f240f', 1);"
    cursor.execute(sql)
    sql = "INSERT INTO `automatic_product`.`interface`(`interface_id`, `interface_name`, `pod_id`, `route_id`, `is_valid`) VALUES ('a66571ff-2224-48de-883e-478b3542fb5a', 'if_two', 'f4e072df-a165-4620-af2c-c2b4a570a107', '164a6d62-7320-49b3-84c6-ccb7f38f240f', 1);"
    cursor.execute(sql)
    raise Exception
except:
    db.rollback()
    traceback.print_exc()
else:
    db.commit()
finally:
    cursor.close()
