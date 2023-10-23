import json
import time
import xlwt
import requests
from lxml import etree
import utils_logger

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

logger = utils_logger.get_logger('py_log', 'INFO')

free_dict = {}
pay_dict = {}
hot_dict = {}


def spider(list, app_list, country_name):
    rank = 0
    app_info_list = []
    for app in app_list:
        if not app.xpath("section[2]/div/h1/a/text()"):
            continue
        app_name = app.xpath("section[2]/div/h1/a/text()")[0]
        company = app.xpath("section[2]/div/h3/a/text()")[0]
        local_rank = app.xpath("section[2]/div/div/span/text()")[0]
        rank += 1
        type_str = ''
        # product_info = app.xpath("section[2]/div/h1/a/@href")[0]
        # product_id = product_info.split('/')[-1]
        # try:
        #     product_info_url = "https://www.baijing.cn/product/ajax/sidebar_product_info/"
        #     data = {'id': product_id}
        #     company_info_res = requests.post(url=product_info_url, data=data, headers=HEADERS, timeout=5)
        #     company_info = json.loads(company_info_res.content)
        #     types = company_info['data']['google']['category']
        #     for type in types:
        #         type_str += " {}".format(type.get('category', ''))
        # except Exception as e:
        #     logger.error("分类信息抓取失败： {} , {}".format(company, product_info_url))
        #     logger.error(e)

        if list == '免费榜':
            free_dict.setdefault(country_name, []).append((rank, app_name, local_rank, company, type_str))
        elif list == '付费榜':
            pay_dict.setdefault(country_name, []).append((rank, app_name, local_rank, company, type_str))
        else:
            hot_dict.setdefault(country_name, []).append((rank, app_name, local_rank, company, type_str))
        logger.info('{} : 第 {} 名， app : {}, 本地榜单第 {} 名，company : {}, type : {}'.format(list, rank, app_name, local_rank,
                                                                                       company, type_str))


country_info_dict = {'荷兰': ('NL', '阿姆斯特丹'), '美国': ('US', '达拉斯、弗吉尼亚、洛杉矶、迈阿密'), '日本': ('JP', '东京'), '德国': ('DE', '法兰克福'),
                     '中国': ('CN', '广州、上海、无锡'), '越南': ('VN', '胡志明'), '法国': ('FR', '马赛'), '印度': ('IN', '孟买'),
                     '巴西': ('BR', '圣保罗'), '韩国': ('KR', '首尔'), '台湾': ('TW', '台北'), '香港': ('HK', '香港'),
                     '新加坡': ('SG', '新加坡'), '印度尼西亚': ('ID', '雅加达')}
fail_list = []

type_list = [('工具', 'TOOLS'), ('社交', 'SOCIAL'), ('图书', 'BOOKS_AND_REFERENCE'), ('娱乐', 'ENTERTAINMENT'), ('教育', 'EDUCATION')]

for type_info in type_list:
    type_name, type_id = type_info

    for country_name, country_info in country_info_dict.items():
        code, city = country_info
        ios_url = 'https://www.baijing.cn/store/?platform=ios&country={}&identifier=iPad&category={}&date=&sort='.format(code, type_id)
        google_url = 'https://www.baijing.cn/store/?platform=google&country={}&identifier=iPhone&category={}&date=&sort='.format(code, type_id)
        try:
            logger.info('开始抓取国家 : {}...'.format(country_name))
            response = requests.get(url=google_url, headers=HEADERS, timeout=3)
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
            spider('免费榜', free_app_list, country_name)
            spider('付费榜', pro_app_list, country_name)
            spider('畅销榜', pop_app_list, country_name)

    logger.info("free : {} \n\n\n".format(free_dict))
    logger.info("pay : {} \n\n\n".format(pay_dict))
    logger.info("hot : {} \n".format(hot_dict))


    def set_style(name, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style


    f = xlwt.Workbook()
    sheet1 = f.add_sheet('免费榜', cell_overwrite_ok=True)
    sheet2 = f.add_sheet('付费榜', cell_overwrite_ok=True)
    sheet3 = f.add_sheet('畅销榜', cell_overwrite_ok=True)
    row0 = ["国家"]
    for index in range(30):
        row0.append('第{}名'.format(index + 1))
    sheet_list = [sheet1, sheet2, sheet3]
    default_style = set_style('Times New Roman', 220, True)
    for i in range(0, len(row0)):
        for sheet in sheet_list:
            sheet.write(0, i, row0[i], default_style)

    row_index = 1
    for country_name, app_list in free_dict.items():
        sheet1.write(row_index, 0, '{}({})'.format(country_name, country_info_dict.get(country_name)[1]), default_style)
        line_index = 1
        for app_info in app_list:
            rank, app_name, local_rank, company, type = app_info
            text = "app name : {}    \r\n分类: {}    \r\n本地排名: {}    \r\n 公司: {}".format(app_name, type, local_rank, company)
            sheet1.write(row_index, line_index, text, default_style)
            line_index += 1

        row_index += 1

    row_index = 1
    for country_name, app_list in pay_dict.items():
        sheet2.write(row_index, 0, '{}({})'.format(country_name, country_info_dict.get(country_name)[1]), default_style)
        line_index = 1
        for app_info in app_list:
            rank, app_name, local_rank, company, type = app_info
            text = "app name : {}    \r\n分类: {}    \r\n本地排名: {}    \r\n 公司: {}".format(app_name, type, local_rank, company)
            sheet2.write(row_index, line_index, text, default_style)
            line_index += 1

        row_index += 1

    row_index = 1
    for country_name, app_list in hot_dict.items():
        sheet3.write(row_index, 0, '{}({})'.format(country_name, country_info_dict.get(country_name)[1]), default_style)
        line_index = 1
        for app_info in app_list:
            rank, app_name, local_rank, company, type = app_info
            text = "app name : {}    \r\n分类: {}    \r\n本地排名: {}    \r\n 公司: {}".format(app_name, type, local_rank, company)
            sheet3.write(row_index, line_index, text, default_style)
            line_index += 1

        row_index += 1

    f.save('{}榜单google.xls'.format(type_name))
