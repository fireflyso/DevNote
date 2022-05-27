import time

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

sql = "INSERT INTO company_info(name, full_name, type_list, financing, address, company_member_count, web_url) VALUES (%s,%s,%s,%s,%s,%s,%s)"


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

logger = utils_logger.get_logger('baijing', 'INFO')
fail_list = []
for index in range(1, 932):
    # index = 1
    url = 'https://www.baijingapp.com/company/page-{}'.format(index)
    try:
        logger.info('开始第 {} 页数据抓取...'.format(index))
        response = requests.get(url=url, headers=HEADERS, timeout=3)
        html = etree.HTML(response.content)
        company_list = html.xpath("//li[@class='cru-list']/div[2]")
        logger.info('抓取成功，随机休眠几秒')
        time.sleep(random.randint(2, 6))
    except BaseException as err:
        logger.info('请求链接：{} 报错'.format(err))
        fail_list.append(index)
        logger.info('失败的页面列表：{}'.format(fail_list))
    else:
        company_info_list = []
        for company in company_list:
            name = ''
            full_name = ''
            type_list = []
            financing = ''
            address = ''
            company_member_count = ''
            web_url = ''
            try:
                name = company.xpath("h2/a/text()")[0]
                full_name = company.xpath("h2/a/@title")[0]
                type_list = company.xpath("div/div/p[1]/text()")[0].split('；')
                # 融资
                financing = company.xpath("div/div/p[2]/text()")[0]
                address = company.xpath("div/div/p[3]/text()")[0].replace('&nbsp', '')
                company_member_count = company.xpath("div/div/p[4]/text()")[0].replace('\t', '')
                web_url = company.xpath("div/div/p[5]/a/text()")[0]
            except Exception as e:
                logger.error("第 {} 页数据处理异常： {}".format(index, e))
            company_info = (name, full_name, ','.join(type_list), financing, address, company_member_count, web_url)
            # logger.info(company_info)
            company_info_list.append(company_info)

        try:
            logger.info(company_info_list)
            cursor.executemany(sql, tuple(company_info_list))
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(e)

db.close()

