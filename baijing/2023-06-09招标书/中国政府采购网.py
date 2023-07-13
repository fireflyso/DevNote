# -- coding: utf-8 --
# @Time : 2023/6/8 18:13
# @Author : xulu.liu
import requests
from lxml import etree
import math
from baijing import utils_logger
import time

logger = utils_logger.get_logger('03', 'INFO')


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1686210040; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1686279641; HMF_CI=1527dbfd2674a4b3683f4e9c37c3c30cddaa864bfba2319f62b032607977403046588e06f6a563b5c234ea05225afa949909c9ab7944067b9437a574670ca8ed9c; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1686281106; JSESSIONID=Fn-fHa6PZuP8v6-WFZZzZgS7KtxfeN9onquanZp2vRc1pLf26sub!-305079923; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1686296703",
    "Host": "search.ccgp.gov.cn",
    "Referer": "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=1&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=IDC&start_time=2022%3A12%3A09&end_time=2023%3A06%3A09&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName=",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"
}
proxies = {
    'http': 'socks5://admin:admin@164.52.47.110:8081',
    'https': 'socks5://admin:admin@164.52.47.110:8081',
}
keyword_list = ['IDC', '数据中心', '智算中心', '超算中心']
base_url = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={}&bidSort={}&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw={}&start_time=2022%3A12%3A09&end_time=2023%3A06%3A09&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName="
type_dict = {'1': '中央公告', '2': '地方公告'}

for keyword in keyword_list:
    for type_no, type_name in type_dict.items():
        logger.info('开始抓取关键字 : {}, 类别 : {}'.format(keyword, type_name))
        total_page = 1
        page_num = 1
        while page_num <= total_page:
            try:
                url = base_url.format(page_num, type_no, keyword)
                res = requests.get(url, timeout=60, headers=HEADERS)
                time.sleep(5)
                html = etree.HTML(res.content)
                res_count = int(html.xpath("//span[@style='color:#c00000']/text()")[0])
                total_page = math.ceil(res_count/20)
                logger.info('共计 {} 页，当前第 {} 页'.format(total_page, page_num))
                page_num += 1
                info_list = html.xpath("//ul[@class='vT-srch-result-list-bid']/li")
                for info in info_list:
                    title_list = [i.replace(' ', '').replace('\r\n', '') for i in info.xpath("a/text()")]
                    title = keyword.join(title_list)
                    time_list = info.xpath("span/text()")[0].replace(' ', '').replace('\r\n', '').split('|')
                    public_time = time_list[0]
                    buyers = time_list[1].replace('采购人：', '')
                    agent_name = time_list[1].replace('代理机构：', '')
                    info_type = info.xpath("span/strong/text()")[0].replace(' ', '').replace('\r\n', '')
                    address = info.xpath("span/a/text()")[0].replace(' ', '').replace('\r\n', '')
                    logger.error('{}, {}, {}, {}, {}, {}, {}'.format(
                        title, public_time, address, info_type, type_name, title, buyers, agent_name
                    ))
            except Exception as e:
                logger.warning(e)
                logger.warning(url)
