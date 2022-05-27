import json
import time

import requests
from lxml import etree
import utils_logger
import random

import pymysql

# 打开数据库连接
db = pymysql.connect(
    host="49.232.142.109",
    user="firefly",
    password="1q2w3e!@#",
    database="cdscp",
    port=3306
)
cursor = db.cursor()

sql = "INSERT INTO rank_info(rank, country, list, app_name, company, type, size) VALUES (%s,%s,%s,%s,%s,%s,%s)"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

logger = utils_logger.get_logger('baijing', 'INFO')
country_dict = {
    '巴西': 'BR',
    '阿根廷': 'AR',
    '哥伦比亚': 'CO',
    '智利': 'CL',
    '秘鲁': 'PE',
    '厄瓜多尔': 'EC',
    '乌拉圭': 'UY',
    '委内瑞拉': 'VE',
    '玻利维亚': 'BO',
    '巴拉圭': 'PY'
}


def spider(list, app_list):
    rank = 0
    app_info_list = []
    for app in app_list:
        if not app.xpath("section[2]/div/h1/a/text()"):
            continue
        app_name = app.xpath("section[2]/div/h1/a/text()")[0]
        company = app.xpath("section[2]/div/h3/a/text()")[0]
        company_url = "https://www.baijingapp.com{}".format(app.xpath("section[2]/div/h3/a/@href")[0])
        rank += 1
        list = list
        country = country_name
        try:
            response = requests.get(url=company_url, headers=HEADERS, timeout=3)
            company_html = etree.HTML(response.content)
            size = company_html.xpath("//p[@class='headinfo']/text()")[0]
            # type = company_html.xpath("//dl/dd/text()")[0]

            company_info_url = "https://www.baijingapp.com/people/ajax/get_company_info/"
            data = {'id' : company_url.split('/')[-1]}
            company_info_res = requests.post(url=company_info_url, data=data, headers=HEADERS, timeout=3)
            company_info = json.loads(company_info_res.content)
            type = company_info['data']['company_info']['company_type_new']
        except Exception as e:
            logger.error("公司信息抓取失败： {} , {}".format(company, company_url))
            logger.error(e)

        company_info = (rank, country, list, app_name, company, type, size)
        logger.info(company_info)
        app_info_list.append(company_info)

    try:
        # logger.info(app_info_list)
        cursor.executemany(sql, tuple(app_info_list))
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(e)

fail_list = []
for country_name, country_code in country_dict.items():
    url = 'https://www.baijingapp.com/store/?platform=ios&country={}&identifier=&category=0&category_name=&date=&sort='.format(country_code)
    try:
        logger.info('开始抓取国家 : {}...'.format(country_name))
        response = requests.get(url=url, headers=HEADERS, timeout=3)
        time.sleep(1)
        html = etree.HTML(response.content)
        free_app_list = html.xpath("//td[@class='free-meat']/div")
        pro_app_list = html.xpath("//td[@class='money-meat']/div")
        pop_app_list = html.xpath("//td[@class='well-meat']/div")
        # logger.info('抓取成功，随机休眠几秒')
        # time.sleep(random.randint(2, 6))
    except BaseException as err:
        logger.info('请求链接：{} 报错'.format(err))
        fail_list.append(country_name)
        logger.info('失败的页面列表：{}'.format(fail_list))
    else:
        spider('免费榜', free_app_list)
        spider('付费榜', pro_app_list)
        spider('畅销榜', pop_app_list)



