import os

import requests

from lxml import etree


def get_page(url, count=0):
    html = None
    try:
        html = requests.get(url=target_url, headers=HEADERS, timeout=5)
    except:
        if count < 3:
            count += 1
            html = get_page(url, count)

    return html

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
keyword = ''
file_name = '美杜莎'
file_name = file_name if file_name else keyword
with open('{}.txt'.format(file_name), 'w+') as f1:
    num = 14355113
    for i in range(1):
        target_url = 'https://www.cool18.com/bbs4/index.php?app=forum&act=threadview&tid={}'.format(num)
        num += 1
        print('准备请求 : {}'.format(target_url))
        html = get_page(target_url)
        if html:
            html = etree.HTML(html.content)
            contents = html.xpath("//pre/text()")
            for content in contents:
                f1.write('{}\n'.format(content.replace('\u3000\u3000', '')))
        else:
            print('  --- 请求失败：{}'.format(target_url))

os.system("scp {} root@alist.liuxulu.top:/data/book".format(file_name))