# -- coding: utf-8 --
# @Time : 2023/12/22 14:26
# @Author : xulu.liu

from Algorithms.sort.base.base import Base


class QuickSort(Base):

    def __init__(self, name='快速'):
        super().__init__(name)

    def aes(self, start=None, end=None):
        start = start if start else 0
        end = end if end else len(self.sort_arr) - 1
        # if start == end:
        #     return
        if start > end:
            return
        base = start
        while start < end:
            for i in range(end, base, -1):
                if self.biger(base, end):
                    self.swap(base, i)
                    base = i
                    break
                end -= 1

            for i in range(start, base):
                if self.less(base, start):
                    self.swap(base, i)
                    base = i
                    break
                start += 1
            print('start : {}, end : {}'.format(start, end))
        self.aes(start, base - 1)
        self.aes(base + 1, end)
        print(self.sort_arr)


