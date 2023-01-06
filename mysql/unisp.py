# coding=utf-8
# 操作线上库，慎用

import pymysql
import traceback

db = pymysql.connect(
    host="write-wangluo-mysql-edge.gic.local",
    user="unisp_wan_status_analysis_write_20221227",
    password="}sUnU<G54I>%mh,SeP",
    database="unisp",
    port=6019,
    charset='utf8'
)

cursor = db.cursor()

# 查询
sql = "UPDATE automatic_product.route SET ip = '148.153.126.177' WHERE route_id = '25a409fa-83b7-4676-a8bd-f2ee47668cf2';"
_ = cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    print("UPDATE automatic_product.subinterface SET interface_id = 'd5fe5c81-e661-483b-9e65-d76aeb6adc3a' WHERE subinterface_id = '{}';".format(r[0]))

# 修改
sql = "insert into fping_product_asn(operator_id, asn, product_id) values (12,17676,3),(9,4713,3),(3,2516,3),(45,17506,3),(36,2907,3),(3,2527,3),(15,9824,3),(3,2518,3),(3,2514,3),(3,2510,3),(30,4766,3),(33,9318,3),(6,17858,3),(39,3786,3),(24,9644,3),(24,18302,3),(42,6619,3),(27,9316,3),(21,9457,3),(18,10036,3);"
cursor.execute(sql)
db.commit()
cursor.close()


