# -- coding: utf-8 --
# @Time : 2023/6/28 10:56
# @Author : xulu.liu

from urlextract import URLExtract

extractor = URLExtract()
url_list = []
with open("/Users/liuxulu/Downloads/运营商.txt") as file:
    for line in file:
        urls = extractor.find_urls(line)
        url = urls[0]
        if '.png' in url:
            url_list.append(url)
            print(url)
print(url_list)
