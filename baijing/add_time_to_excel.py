import xlrd
import requests
from lxml import etree
from xlutils.copy import copy
import utils_logger
import time, re


def get_str(content, startStr, endStr):
    patternStr = r'%s(.+?)%s' % (startStr, endStr)
    p = re.compile(patternStr, re.IGNORECASE)
    m = re.match(p, content)
    if m:
        return m.group(1)

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
logger = utils_logger.get_logger('baijing', 'INFO')
new_company_list = []
workbook = xlrd.open_workbook('./list.xls')  # 打开工作簿
sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
new_excel = copy(workbook)
table = new_excel.get_sheet(0)
table.write(0, 7, '成立时间')
fail_list = []
for i in range(1, worksheet.nrows):
    company_name = worksheet.cell_value(i, 1)
    logger.info('开始抓取  {} 的简介'.format(company_name))
    url = 'https://baike.baidu.com/item/{}'.format(company_name)
    try:
        detail_str = ''
        # response = requests.get(url=url, headers=HEADERS, timeout=3, proxies={'http': '127.0.0.1:8118'})
        response = requests.get(url=url, headers=HEADERS, timeout=3)
        html = etree.HTML(response.content)
        detail_str = ('').join(html.xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]//text()'))
        detail_str = re.sub(u"\\[.*?]", "", detail_str).replace('\n', '').replace('\xa0', '')
        if '成立时间' in detail_str:
            build_time = detail_str.split('成立时间')[1].split('日')[0] + '日'
            logger.info('{} 成立时间 : {}'.format(company_name, build_time))
            table.write(i, 7, build_time)
        else:
            logger.info('{} 没有找到成立时间信息'.format(company_name))
        time.sleep(0.5)
    except BaseException as err:
        logger.info('请求链接：{} 报错'.format(err))
        fail_list.append(company_name)
        logger.info('失败的页面列表：{}'.format(fail_list))

new_excel.save("company_info.xls")