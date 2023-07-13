# -- coding: utf-8 --
# @Time : 2023/3/31 16:13
# @Author : xulu.liu

import tracemalloc

tracemalloc.start()

a = ['1234567890' for _ in range(10000)]
b = ['1234567890' for _ in range(100000)]
c = ['1234567890' for _ in range(1000000)]
d = ['1234567890' for _ in range(10000000)]

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)

a: str

