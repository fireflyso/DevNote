# -- coding: utf-8 --
# @Time : 2023/2/13 11:47
# @Author : xulu.liu
# @File : 官网关键字查询.py
# @Software: PyCharm
from baijing import utils_logger
from lxml import etree
import requests
import queue
from bs4 import BeautifulSoup


logger = utils_logger.get_logger('home_search', 'INFO')

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
keyword = '超级计算'
# keyword = '弹性计算'
start_url = 'https://www.capitalonline.net.cn/'
base_url = 'https://www.capitalonline.net.cn'
q = queue.Queue()
q.put(start_url)
targe_url_set = set()
checked_url_list = []
all_url_list = []


def spider(search_url):
    try:
        checked_url_list.append(search_url)
        response = requests.get(url=search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        if keyword in soup.text:
            targe_url_set.add(search_url)
            logger.info('页面 : {} 发现关键字 : {}, 页面列表：'.format(search_url, keyword))
            for url in targe_url_set:
                logger.info(url)

        html = etree.HTML(response.content)
        urls = html.xpath("//a/@href")
        for url in urls:
            if url == '/' or url.endswith('.pdf') or url.endswith('.docx') or url.endswith('.zip'):
                continue
            if url.startswith('/'):
                temp_url = '{}{}'.format(base_url, url)
                if temp_url not in all_url_list:
                    q.put(temp_url)
                    all_url_list.append(temp_url)
            elif url.startswith('https') and 'capitalonline' in url:
                temp_url = url
                if temp_url not in all_url_list:
                    q.put(temp_url)
                    all_url_list.append(temp_url)
    except Exception as e:
        logger.exception(e)
        logger.error('页面解析异常 : {}'.format(search_url))

    checked_count = len(checked_url_list)
    logger.info('共发现 {} 个页面, 已检测 {} 个页面，锁定 {} 个目标页面! 当前解析 : {}'.format(
        len(all_url_list), checked_count, len(targe_url_set), search_url))


if __name__ == '__main__':
    while q.qsize() > 0:
        search_url = q.get()
        spider(search_url)

    logger.info(' --- 检索结束 ---')
    checked_count = len(checked_url_list)
    logger.info('共发现 {} 个页面, 已检测 {} 个页面，锁定 {} 个目标页面！'.format(
        len(all_url_list), checked_count, len(targe_url_set)))
    logger.info('目标页面列表 : {}'.format(targe_url_set))

