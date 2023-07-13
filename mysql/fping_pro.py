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


id_list = [65, 467, 54, 469, 470, 471, 472, 473, 474, 475, 476, 595, 721]
id_dict = {65: 'PT XL Axiata(24203)' , 467: 'Telkomsel(23693)' , 54: 'Telekomunikasi Indonesia (7713)' , 469: 'Indosat Ooredoo(4761)' , 470: 'Telkom Indonesia(17974)' , 471: 'IndosatM2(4795)' , 472: 'Link Net(23700)' , 473: 'Biznet(17451)' , 474: 'Lintasarta(4800)' , 475: 'Jetcoms Netindo(17671)' , 476: 'CBN(4787)' , 595: 'Hutchison CP Telecommunications(45727)' , 721: 'PT WIRELESS INDONESIA(18004)'}
for pid, name in id_dict.items():
    print('运营商 : {}'.format(name))
    sql = "select operator_id, start_ip, end_ip from sub_net where operator_id = {} and is_valid = 1 and country = '印度尼西亚' limit 30;".format(pid)
    _ = cursor.execute(sql)
    res = cursor.fetchall()
    for r in res:
        print('{}/24'.format(r[1]))


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


sql = "UPDATE wanfping.product_vm SET name = '马赛BGP', is_valid = 0 WHERE id = 50;"
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
