import requests
from lxml import etree
import utils_logger
import random

import pymysql

# 打开数据库连接
db = pymysql.connect(
    host="103.229.214.35",
    user="firefly",
    password="cds-cloud@2017",
    database="flow_data",
    port=3306
)
cursor = db.cursor()

sql = 'select * from company_info where id > 9060'
res = cursor.execute(sql)
res_list = cursor.fetchall()
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

print("公司数量： {}".format(len(res_list)))
row = 0
for company_info in res_list:
    if not company_info[8]:
        # url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query=".format(company_info[1])
        url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query=".format('白鲸出海')
        response = requests.get(url=url, headers=HEADERS, timeout=3)
        html = etree.HTML(response.content)
        company_info = html.xpath("//dd//text()")
        import pdb
        pdb.set_trace()
        print(company_info)
        break