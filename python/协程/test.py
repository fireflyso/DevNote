# -- coding: utf-8 --
# @Time : 2023/9/5 11:37
# @Author : xulu.liu
import asyncio
import aiohttp
import time
import json

start = time.time()


async def get_page(url):
    print("开始爬取网站", url)
    # 异步块，在执行异步方法的时候加上await才能切换，不然就是串行咯
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with await session.get(url) as resp:
            page = await resp.text()
    return page


async def request():
    url = 'https://httpbin.org/delay/5'
    print('Waiting for', url)
    # data = await get(url)
    data = await get_page(url)
    data = json.loads(data).get('origin', '')
    return data

tasks = [asyncio.ensure_future(request()) for _ in range(100)]
loop = asyncio.get_event_loop()
datas, _ = loop.run_until_complete(asyncio.wait(tasks))
for data in datas:
    print(data.result())

end = time.time()
print('Cost time:', end - start)
