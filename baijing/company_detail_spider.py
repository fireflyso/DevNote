import re
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


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

logger = utils_logger.get_logger('baijing', 'INFO')
fail_list = []

sql = 'select * from company_info where id > 9084'
res = cursor.execute(sql)
res_list = cursor.fetchall()

logger.info("公司数量： {}".format(len(res_list)))
for company_info in res_list:
    company_name = company_info[1]
    logger.info('开始抓取  {} 的简介'.format(company_name))
    url = 'https://baike.baidu.com/item/{}'.format(company_name)
    try:
        detail_str = ''
        # response = requests.get(url=url, headers=HEADERS, timeout=3, proxies={'http': '127.0.0.1:8118'})
        response = requests.get(url=url, headers=HEADERS, timeout=3)
        html = etree.HTML(response.content)
        detail_str = ('').join(html.xpath('//div[@class="lemma-summary"]//text()'))
        detail_str = re.sub(u"\\[.*?]", "", detail_str).replace('\n', '').replace('\xa0', '')
        time.sleep(1)
    except BaseException as err:
        logger.info('请求链接：{} 报错'.format(err))
        logger.info('失败的页面列表：{}'.format(fail_list))
    else:
        try:
            if detail_str:
                logger.info(detail_str)
                sql = "UPDATE `flow_data`.`company_info` SET `desc` = '{}' WHERE `id` = {}".format(
                    detail_str, company_info[0])
                cursor.execute(sql)
                db.commit()
        except Exception as e:
            db.rollback()
            logger.error(e)

    # company_name = company_info[2]
    # logger.info('开始抓取  {} 的全名简介'.format(company_name))
    # url = 'https://baike.baidu.com/item/{}'.format(company_name)
    # try:
    #     detail_str = ''
    #     response = requests.get(url=url, headers=HEADERS, timeout=3, proxies={'http': '127.0.0.1:8118'})
    #     html = etree.HTML(response.content)
    #     detail_str = ('').join(html.xpath('//div[@class="lemma-summary"]//text()'))
    #     detail_str = re.sub(u"\\[.*?]", "", detail_str).replace('\n', '').replace('\xa0', '')
    #     time.sleep(0.1)
    # except BaseException as err:
    #     logger.info('请求链接：{} 报错'.format(err))
    #     logger.info('失败的页面列表：{}'.format(fail_list))
    # else:
    #     try:
    #         if detail_str:
    #             logger.info(detail_str)
    #             sql = "UPDATE `flow_data`.`company_info` SET `desc_full` = '{}' WHERE `id` = {}".format(
    #                 detail_str, company_info[0])
    #             cursor.execute(sql)
    #             db.commit()
    #     except Exception as e:
    #         db.rollback()
    #         logger.error(e)

db.close()

