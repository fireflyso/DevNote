import utils_logger
import xlwt
import time
from lxml import etree
import requests
logger = utils_logger.get_logger('baijing', 'INFO')
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


def spider(list, app_list, country_name):
    rank = 0
    for app in app_list:
        if not app.xpath("section[2]/div/h1/a/text()"):
            continue
        app_name = app.xpath("section[2]/div/h1/a/text()")[0]
        company = app.xpath("section[2]/div/h3/a/text()")[0]
        local_rank = app.xpath("section[2]/div/div/span/text()")[0]
        rank += 1
        type_str = ''
        if list == '免费榜':
            free_dict.setdefault(country_name, []).append((rank, app_name, local_rank, company, type_str))
        elif list == '付费榜':
            pay_dict.setdefault(country_name, []).append((rank, app_name, local_rank, company, type_str))
        else:
            hot_dict.setdefault(country_name, []).append((rank, app_name, local_rank, company, type_str))
        logger.info('{} : 第 {} 名， app : {}, 本地榜单第 {} 名，company : {}, type : {}'.format(
            list, rank, app_name, local_rank, company, type_str))


def get_home_page():
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
    else:
        spider('免费榜', free_app_list, country_name)
        spider('付费榜', pro_app_list, country_name)
        spider('畅销榜', pop_app_list, country_name)


def write_sheet(rank_dict, row_index):
    if not rank_dict:
        return row_index

    for country_name, app_list in rank_dict.items():
        sheet.write(row_index, 0, country_name, default_style)
        sheet.write(row_index, 1, platform_type, default_style)
        sheet.write(row_index, 2, rank_type, default_style)
        line_index = 3
        for app_info in app_list:
            rank, app_name, local_rank, company, type = app_info
            text = "app name : {}    \r\n本地排名: {}    \r\n 公司: {}".format(app_name, local_rank, company)
            sheet.write(row_index, line_index, text, default_style)
            line_index += 1

    return row_index + 1


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


if __name__ == '__main__':
    type_info = {
        '游戏排行榜': (6014, 'GAME'),
        '图书排行榜': (6018, 'BOOKS_AND_REFERENCE'),
        '工具排榜单': (6002, 'TOOLS'),
        '旅游排行榜': (6003, ''),
        '教育排行榜': (6017, 'EDUCATION'),
        '社交排行榜': (6005, 'SOCIAL'),
        '娱乐排行榜': (6016, 'ENTERTAINMENT'),
    }
    country_code_dict = {'新加坡(新加坡)': 'SG', '美国(达拉斯、弗吉尼亚、洛杉矶、迈阿密)': 'US', '德国(法兰克福)': 'DE', '台湾(台北)': 'TW', '巴西(圣保罗)': 'BR', '印度尼西亚(雅加达)': 'ID', '印度(孟买)': 'IN', '越南(胡志明)': 'VN', '中国(广州、上海、无锡)': 'CN', '日本(东京)': 'JP', '香港(香港)': 'HK', '荷兰(阿姆斯特丹)': 'NL', '韩国(首尔)': 'KR'}

    google_url = 'https://www.baijing.cn/store/?platform=google&country={}&identifier=iPhone&category={}&date=1672848000&sort='
    ios_url = 'https://www.baijing.cn/store/?platform=ios&country={}&identifier=iPad&category={}&date=1672848000&sort='

    row_temp = ["国家", '平台', '榜单类型']
    for index in range(30):
        row_temp.append('第{}名'.format(index + 1))

    default_style = set_style('Times New Roman', 220, True)

    f = xlwt.Workbook()
    for sheet_name, info in type_info.items():
        ios_type, google_type = info
        sheet = f.add_sheet(sheet_name, cell_overwrite_ok=True)
        for i in range(0, len(row_temp)):
            sheet.write(0, i, row_temp[i], default_style)

        row_index = 1
        for country_name, country_code in country_code_dict.items():
            # 抓取ios信息
            free_dict = {}
            pay_dict = {}
            hot_dict = {}
            platform_type = 'Apple store'
            url = ios_url.format(country_code, ios_type)
            get_home_page()

            rank_type = '免费'
            row_index = write_sheet(free_dict, row_index)
            rank_type = '付费'
            row_index = write_sheet(pay_dict, row_index)
            rank_type = '畅销'
            row_index = write_sheet(hot_dict, row_index)

            # 抓取ios信息
            free_dict = {}
            pay_dict = {}
            hot_dict = {}
            platform_type = 'Google Play'
            if google_type:
                url = google_url.format(country_code, google_type)
                get_home_page()

                rank_type = '免费'
                row_index = write_sheet(free_dict, row_index)
                rank_type = '付费'
                row_index = write_sheet(pay_dict, row_index)
                rank_type = '畅销'
                row_index = write_sheet(hot_dict, row_index)

    f.save('排行榜.xls')


