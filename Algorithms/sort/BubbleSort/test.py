# -- coding: utf-8 --
# @Time : 2023/12/21 18:46
# @Author : xulu.liu

sort_arr = [23, 5, 8, 122, 32, 45, 72, 342, 2, 89, 12, 34, 11, 9, 77]
count = len(sort_arr)
for i in range(1, count):
    while i > 0 and sort_arr[i] < sort_arr[i - 1]:
        sort_arr[i], sort_arr[i - 1] = sort_arr[i - 1], sort_arr[i]
        i -= 1
    print(sort_arr)

print(sort_arr)
