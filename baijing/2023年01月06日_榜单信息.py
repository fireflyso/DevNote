import utils_logger
import xlwt
logger = utils_logger.get_logger('baijing', 'INFO')


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

    free_dict = {}
    pay_dict = {}
    hot_dict = {}


