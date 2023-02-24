# -- coding: utf-8 --
# @Time : 2023/2/15 14:23
# @Author : xulu.liu
# @File : video_spider.py
# @Software: PyCharm
import requests
import re
import os
import threading
import queue


# 从网页上复制下来的请求头
headers = {
    'authority': 'cdn3.jiuse.cloud',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6'
}


def download_ts():
    # 获取m3u8文件
    res = requests.get(url).text
    # 正则提取内容
    ts = re.findall(r"(\d+).ts", res, flags=re.S)
    print('初始化任务列表 : {}'.format(ts))
    for t in ts:
        task_queue.put(t)

    thread_list = []
    for i in range(10):
        t = threading.Thread(target=worker)
        t.start()
        thread_list.append(t)

    print('多线程开启完成!')

    for t in thread_list:
        t.join()

    sort_ts(ts)


def worker():
    while task_queue.qsize() > 0:
        index = task_queue.get()
        # 拼接完整的ts文件下载链接
        u = url_prifix + index + ".ts"
        r = requests.get(url=u, headers=headers).content
        print(index, u)
        # 二进制写入到本地
        with open('./ts/' + index + '.ts', mode="wb") as file:
            file.write(r)
    print('work任务结束!')


def clear_dir():
    print('清理ts文件夹')
    os.system("rm -rf ts/*")

    if os.path.exists('all.mp4'):
        print('清理mp4文件')
        os.system("rm -rf all.mp4")

    if os.path.exists('all.ts'):
        print('清理ts文件')
        os.system("rm -rf all.ts")


def sort_ts(ts):
    for t in ts:
        os.system("setfile -d '1/1/2023 1:0:{}' ./ts/{}.ts".format(t, t))
        os.system("setfile -m '1/1/2023 1:0:{}' ./ts/{}.ts".format(t, t))



task_queue = queue.Queue()
url = "https://cdn3.jiuse.cloud/hls/747452/index.m3u8?t=1676617379&m=9EdqC9U3mOE9f2xAQOrRTQ"
url_prifix = "{}index".format(url.split('index.')[0])
file_name = "{}.mp4".format(url.split('/')[-2])

if __name__ == '__main__':
    print('开始执行抓取任务')
    clear_dir()
    download_ts()
    # 利用cmd命令将.ts文件合成为mp4格式
    os.system("cat ts/*.ts > all.ts")
    os.system("ffmpeg -i all.ts -map 0 -c copy {}".format(file_name))
    print("转换成功")
    os.system("mv {} source".format(file_name))
    os.system("rm -rf ts/*")
