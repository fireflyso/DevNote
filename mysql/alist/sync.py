# -- coding: utf-8 --
# @Time : 2023/11/13 18:36
# @Author : xulu.liu
import pymysql
from datetime import datetime, timedelta

cds_db = pymysql.connect(
    host="10.13.132.242",
    user="jichu_wangluo",
    password="VTuzl1iwTTkGNAzc",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cds_cursor = cds_db.cursor()

alist_db = pymysql.connect(
    host="alist.liuxulu.top",
    user="firefly",
    password="cds-cloud@2017",
    database="django_test",
    port=5703,
    charset='utf8'
)

alist_cursor = alist_db.cursor()


def sync_bill():
    start_time = datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    while start_time < datetime.now():
        print(start_time)
        end_time = start_time + timedelta(days=1)
        sql = "select sum(cost) from bc_bill_detail where start_time >= '{}' and start_time < '{}' and cost > 0;".format(
            start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')
        )
        _ = cds_cursor.execute(sql)
        res = cds_cursor.fetchall()
        bill_cost = int(res[0][0])
        insert_sql = "insert into cloud_bill(bill_date, total_bill) values('{}', {});".format(
            start_time, bill_cost
        )
        alist_cursor.execute(insert_sql)
        start_time = end_time
    alist_db.commit()


sync_bill()
