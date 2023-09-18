# -- coding: utf-8 --
# @Time : 2023/9/5 17:11
# @Author : xulu.liu
import asyncio
import json
import time

import aiohttp


async def batch_process_task(tasks, batch_size=10):
    # 将任务列表划分为多个批次
    result_list = []
    for i in range(0, len(tasks), batch_size):
        print(i)
        batch = tasks[i:i + batch_size]
        # 使用原生协程来异步处理每个批次的任务
        result = await asyncio.gather(*[process_task(task) for task in batch])
        result_list += result
    return result_list


async def process_task(task):
    print("开始爬取网站: {}".format(task))
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with await session.get(task) as resp:
            page = await resp.text()
    return page


async def main():
    # 构造任务列表
    url = 'https://httpbin.org/delay/5'
    tasks = [url for _ in range(20)]
    # 并发处理批量任务
    result_list = await batch_process_task(tasks, batch_size=10)
    return result_list


if __name__ == '__main__':
    start = time.time()
    result_list = asyncio.run(main())
    for data in result_list:
        print(json.loads(data).get('origin', ''))
    end = time.time()
    print('Cost time:', end - start)

