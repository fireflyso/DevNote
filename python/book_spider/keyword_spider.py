import requests

from lxml import etree

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
base_url = 'https://www.cool18.com/bbs4/'
keyword = '无间行者'
url = 'https://www.cool18.com/bbs4/index.php?act=threadsearch&app=forum&keywords={}&submit=栏目搜索'.format(keyword)
print('准备请求 : {}'.format(url))
html = requests.get(url=url, headers=HEADERS, timeout=5)
html = etree.HTML(html.content)
pages = html.xpath("//span[@class='t_subject']/a/@href")
with open('{}.txt'.format(keyword), 'w+') as f1:
    for page_url in reversed(pages):
        target_url = '{}{}'.format(base_url, page_url)
        print('准备请求 : {}'.format(target_url))
        html = requests.get(url=target_url, headers=HEADERS, timeout=5)
        html = etree.HTML(html.content)
        contents = html.xpath("//pre/text()")
        for content in contents:
            f1.write('{}\n'.format(content.replace('\u3000\u3000', '')))
