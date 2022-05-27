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

sql = "INSERT INTO active_info(name, active_url, img_url, time, view_count, member_count) VALUES (%s,%s,%s,%s,%s)"


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

logger = utils_logger.get_logger('baijing', 'INFO')
fail_list = []
for index in range(1, 64):
    # index = 1
    url = 'https://www.baijingapp.com/activity/page-{}'.format(index)
    try:
        logger.info('开始第 {} 页数据抓取...'.format(index))
        response = requests.get(url=url, headers=HEADERS, timeout=3)
        html = etree.HTML(response.content)
        active_list = html.xpath("//div[@class='content-box-row']")
        logger.info('抓取成功，随机休眠几秒')
        time.sleep(random.randint(1, 2))
    except BaseException as err:
        logger.info('请求链接：{} 报错'.format(err))
        fail_list.append(index)
        logger.info('失败的页面列表：{}'.format(fail_list))
    else:
        active_info_list = []
        for company in active_list:
            name = ''
            active_url = ''
            img_url = ''
            creat_time = []
            view_count = 0
            member_count = 0
            try:
                name = company.xpath("div[1]/a/img/@alt")[0].strip()
                active_url = 'https://www.baijingapp.com'+company.xpath("div[1]/a/@href")[0].strip()
                img_url = 'https://www.baijingapp.com'+company.xpath("div[1]/a/img/@src")[0].strip()
                creat_time = company.xpath("div[2]/div[1]/text()")[1].strip().replace('\t', '')
                view_count = int(company.xpath("div[2]/div[2]/text()")[1].strip().replace('\t', ''))
                member_count = int(company.xpath("div[2]/div[3]/text()")[1].strip().replace('\t', ''))
            except Exception as e:
                logger.error("第 {} 页数据处理异常： {}".format(index, e))
            company_info = (name, active_url, img_url, creat_time, view_count, member_count)
            # logger.info(company_info)
            active_info_list.append(company_info)

        try:
            logger.info(active_info_list)
            cursor.executemany(sql, tuple(active_info_list))
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(e)

db.close()

