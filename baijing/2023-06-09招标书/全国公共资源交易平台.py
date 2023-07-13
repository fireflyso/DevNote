# -- coding: utf-8 --
# @Time : 2023/6/8 18:13
# @Author : xulu.liu
import requests
import json
from baijing import utils_logger
import time
import random

logger = utils_logger.get_logger('baijing', 'INFO')

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Length": "291",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "JSESSIONID=e27f0938973bdb249f5b65b34a7b; insert_cookie=67313298",
    "Host": "deal.ggzy.gov.cn",
    "Origin": "http://deal.ggzy.gov.cn",
    "Referer": "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58",
    "X-Requested-With": "XMLHttpRequest"
}

keyword_list = ['IDC', '数据中心', '智算中心', '超算中心']
url = 'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp'
business_type_list = ['招标公告', '开标记录', '评标公示', '中标公告', '签约履行']
# SOURCE_TYPE
platform_info = {
    '1': {
        'name': '省平台',
        'DEAL_CLASSIFY': '00',
        'type_info': {'0001': '交易公告', '0002': '成交公示'}   # DEAL_STAGE
    },
    '2': {
        'name': '央企招投标',
        'DEAL_CLASSIFY': '01',
        'type_info': {'0101': '招标/资审公告', '0102': '开标记录', '0104': '交易结果公示', '0105': '招标/资审文件澄清'}
    },
}
for keyword in keyword_list:
    for source_no, source_info in platform_info.items():
        platform_name = source_info['name']
        deal_classify = source_info['DEAL_CLASSIFY']
        type_info = source_info['type_info']
        for type_no, type_name in type_info.items():
            logger.info('开始抓取关键字 : {}, 平台 : {}, 分类 : {}'.format(keyword, platform_name, type_name))
            data = {
                "TIMEBEGIN_SHOW": "2023-05-31",
                "TIMEEND_SHOW": "2023-06-09",
                "TIMEBEGIN": "2023-05-31",
                "TIMEEND": "2023-06-09",
                "SOURCE_TYPE": source_no,
                "DEAL_TIME": "05",
                "DEAL_CLASSIFY": deal_classify,
                "DEAL_STAGE": type_no,
                "DEAL_PROVINCE": "0",
                "DEAL_CITY": "0",
                "DEAL_PLATFORM": "0",
                "BID_PLATFORM": "0",
                "DEAL_TRADE": "0",
                "isShowAll": "1",
                "PAGENUMBER": "1",
                "FINDTXT": keyword
            }
            total_page = 1
            page_num = 1
            while page_num <= total_page:
                try:
                    data['PAGENUMBER'] = str(page_num)
                    res = requests.post(url, data=data, timeout=60, headers=HEADERS)
                    page_num += 1
                    time.sleep(random.randint(1, 3))
                    res_data = json.loads(res.content)
                    info_list = res_data['data']
                    total_page = res_data['ttlpage']
                    logger.info('共计 {} 页，当前第 {} 页'.format(total_page, page_num))

                    for info in info_list:
                        logger.error('{}, {}, {}, {}, {}, {}, {}'.format(
                            info['title'], info['timeShow'], info['districtShow'], info['stageShow'], platform_name,
                            info['title'], info['platformName']
                        ))
                except Exception as e:
                    logger.warn(e)
