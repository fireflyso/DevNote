# -- coding: utf-8 --
# @Time : 2023/3/10 11:39
# @Author : xulu.liu
# @File : fping覆盖数据统计.py
# @Software: PyCharm
import pymysql
import time
from clickhouse_driver import Client

CK_HOST = "10.13.124.35"    # 节点1
CK_USER = "default"
CK_PASSWORD = "$nM*Jgkx%DmU"
CK_DB_ANME = "wan_fping"
CK_PORT = 9000
client = Client(host="10.13.124.35", port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DB_ANME)

db = pymysql.connect(
    host="write-wangluo-mysql-edge.gic.local",
    user="unisp_wan_status_analysis_write_20221227",
    password="}sUnU<G54I>%mh,SeP",
    database="unisp",
    port=6019,
    charset='utf8'
)

cursor = db.cursor()

pid_list = [('24', '雅加达多线BGP', '148.153.100.194'), ('21', '新加坡经济型BGP', '148.153.146.54'), ('26', '达拉斯覆盖墨西哥', '148.153.122.6'), ('16', '达拉斯VIP专用宽带', '148.153.48.206'), ('20', '迈阿密BPG', '148.153.168.204'), ('10', '法兰克福BGP', '148.153.82.18'), ('11', '达拉斯BGP', '148.153.65.178'), ('19', '台北BGP中国优化', '164.52.9.118'), ('23', '胡志明本地多线BGP', '42.115.66.38'), ('9', '东京BPG', '164.52.25.158'), ('13', '孟买BGP', '164.52.120.134'), ('17', '弗吉尼亚BGP', '148.153.160.146'), ('5', '新加坡BGP', '164.52.2.166'), ('18', '上海单电信', '101.89.89.82'), ('6', '广州BGP', '103.228.162.142'), ('4', '北京BGP', '106.3.133.86'), ('8', '香港BGP', '164.52.12.14'), ('22', '圣保罗BGP', '148.153.200.42'), ('14', '阿姆斯特丹BGP', '148.153.25.234'), ('7', '无锡BGP', '163.53.169.254'), ('15', '洛杉矶BGP', '148.153.44.206'), ('3', '首尔BGP', '164.52.42.110'), ('12', '台北VIP专用带宽', '150.116.92.50')]
pid_list = [('20', '迈阿密BPG', '148.153.168.204'), ('10', '法兰克福BGP', '148.153.82.18'), ('11', '达拉斯BGP', '148.153.65.178'), ('5', '新加坡BGP', '164.52.2.166'), ('22', '圣保罗BGP', '148.153.200.42')]

for pid_info in pid_list:
    pid = int(pid_info[0])
    name = pid_info[1]
    public_ip = pid_info[2]

    ck_res = client.execute(
        "select asn, count(distinct prefixes), count(distinct dst_ip) from wan_fping.fping_data_all where src_ip = toIPv4('{}') and ping_time > '2023-03-10 10:57:41' group by asn;".format(
            public_ip))

    ck_info = {}
    for ck_r in ck_res:
        ck_info[ck_r[0]] = (ck_r[1], ck_r[2])

    sql = "select a.asn, count(b.id) from fping_product_asn a left join fping_prefixes b on a.asn = b.asn and b.is_valid = 1 where a.product_id = {} and a.is_valid = 1  group by a.asn;".format(pid)
    _ = cursor.execute(sql)
    res = cursor.fetchall()
    print('产品 {} ({}) 信息统计！'.format(pid, name))
    for r in res:
        asn = r[0]
        db_prefixe_count = r[1]
        ck_prefixes, ck_ips = ck_info.get(asn, (0, 0))
        # print('asn : {}, db_prefixe_count : {}, ck_prefixe_count : {}, ck_ip_count : {}'.format(asn, db_prefixe_count, ck_prefixes, ck_ips))
        print('{}, {}, {}, {}'.format(asn, db_prefixe_count, ck_prefixes, ck_ips))

    print('\n\n\n\n\n')
    time.sleep(30)






