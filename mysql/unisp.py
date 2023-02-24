# coding=utf-8
# unisp,二期网络质量覆盖

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
sql = "select asn, operator_id, count(0) as count from fping_asn group by asn, operator_id having count > 1 order by asn;"
_ = cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    asn = r[0]
    operator_id = r[1]
    count = r[2]
    query_sql = 'select id from fping_asn where operator_id = {} and asn = {} order by id limit 1;'.format(operator_id, asn)
    _ = cursor.execute(query_sql)
    asn_id = cursor.fetchall()[0][0]
    delete_sql = "update fping_asn set is_valid = 0 where operator_id = {} and asn = {} and id != {}".format(operator_id, asn, asn_id)
    cursor.execute(delete_sql)

db.commit()
cursor.close()

# 修改
import json
data = {"prefixes_spider_thread_count": 5, "ip_spider_thread_count": 100, "fping_spider_thread_count": 30, "mtr_spider_thread_count": 300}
data = json.dumps(data)
sql = "UPDATE unisp.fping_product SET proxy_api = 'http://148.153.54.93:30110' WHERE id = 26;"
cursor.execute(sql)
db.commit()
cursor.close()


