# coding=utf-8
# 操作线上库，慎用
import pymysql
import traceback

db = pymysql.connect(
    host="10.13.103.130",
    user="gwfg_20210113",
    password="@$4%95qXHa%VlO27k7hR",
    database="wanfping",
    port=3306,
    charset='utf8'
)

cursor = db.cursor()


sql = "UPDATE wanfping.product_vm SET nickname = 'BGP(经济型多线)' WHERE id = 34;"
cursor.execute(sql)
db.commit()
sql = "UPDATE wanfping.product_vm SET nickname = '单电信' WHERE id = 35;"
cursor.execute(sql)
db.commit()
sql = "UPDATE wanfping.product_vm SET nickname = 'BGP(经济型多线)' WHERE id = 28;"
cursor.execute(sql)
db.commit()
sql = "UPDATE wanfping.product_vm SET nickname = 'BGP(本地多线)' WHERE id = 11;"
cursor.execute(sql)
db.commit()

try:
    pass
except:
    db.rollback()
    traceback.print_exc()
finally:
    cursor.close()
