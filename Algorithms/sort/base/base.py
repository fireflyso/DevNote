# -*- coding: utf-8 -*-

class Base:
    sort_arr = [23, 5, 8, 122, 32, 45, 72, 342, 2, 89, 12, 34, 11, 9, 77]
    sort_model = [23, 5, 8, 122, 32, 45, 72, 342, 2, 89, 12, 34, 11, 9, 77]

    action_times = 0

    def __init__(self, name="玄学"):
        self.name = name
        print("    --- 开始进行 {} 排序 ---".format(self.name))
        print("排序前的数组为: {}\n".format(self.sort_model))

    def less(self, a, b):
        self.action_times += 1
        return self.sort_arr[a] < self.sort_arr[b]

    def biger(self, a, b):
        self.action_times += 1
        return self.sort_arr[a] > self.sort_arr[b]

    def swap(self, a, b):
        self.action_times += 1
        temp = self.sort_arr[a]
        self.sort_arr[a] = self.sort_arr[b]
        self.sort_arr[b] = temp

    def sort_aes(self):
        print("排列顺序：升序排列")
        self.aes()
        self.show_res()

    def sort_des(self):
        print("排列顺序：降序排列")
        self.des()
        self.show_res()

    def aes(self):
        print("{}排序的升序排序方法还未实现".format(self.name))
        pass

    def des(self):
        print("{}排序的降序排序方法还未实现".format(self.name))
        pass

    def show_res(self):
        print("本次操作的时间复杂度为: {}".format(self.action_times))
        print("排序后的数组为: {}\n".format(self.sort_arr))
        # 重置sort_arr到排序前的状态,且保持arr和model的内存独立
        self.sort_arr = self.sort_model[:]
