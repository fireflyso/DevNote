import asyncio
import time
import queue
import random


class AsyncTest:

    def __init__(self):
        self.proxy_que = queue.Queue(maxsize=100)
        self.init_que()

    def init_que(self):
        for i in range(50):
            self.proxy_que.put(i)

    def start(self):
        while True:
            asyncio.run(self.main(self.proxy_que))

    async def say_after(self, proxy, proxy_que):
        print(f"started at {time.strftime('%X')} - proxy {proxy}")
        # print("proxy : {}".format(proxy))
        delay = random.randint(1, 3)
        await asyncio.sleep(delay)
        proxy_que.put(proxy)

    async def main(self, proxy_que):
        task_list = []
        while not proxy_que.empty():
            proxy = proxy_que.get()
            task = asyncio.create_task(self.say_after(proxy, proxy_que))
            task_list.append(task)

        for task in task_list:
            await task

        print("代理使用完成，本轮任务结束")


if __name__ == '__main__':
    test = AsyncTest()
    test.start()
