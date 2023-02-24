# coding=utf-8
# fping一期线上数据库
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


id_list = [9,10,11,12,13,14,44,91,90,89,93,94,95,96,97,99,100,101,103]
for pid in id_list:
    sql = "INSERT INTO wanfping.fping_group_vm (create_time, update_time, is_valid, fping_group_id, product_vm_id) VALUES ('2022-10-18 14:29:47', '2022-10-18 14:29:47', 1, {}, 56);".format(pid)
    print(sql)
    cursor.execute(sql)

sql = "select a.id, a.name, a.nickname, b.name from product_vm a, site b where a.site_id = b.id and a.company = 'cds';"

_ = cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    id = r[0]
    nickname = r[2]
    site_name = r[3]
    nickname = "{}-{}".format(site_name.replace('节点', ''), nickname)
    sql = "UPDATE wanfping.product_vm SET nickname = '{}' WHERE id = {};".format(nickname, id)
    print(sql)
    cursor.execute(sql)


sql = "UPDATE wanfping.product_vm SET nickname = '胡志明-临时测试', company = 'cds' WHERE id = 57;"
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
