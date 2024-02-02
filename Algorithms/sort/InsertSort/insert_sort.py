# -*- coding: utf-8 -*-
from Algorithms.sort.base.base import Base


class InsertSort(Base):

    def __init__(self, name="插入"):
        super().__init__(name)

    def aes(self):
        arr_len = len(self.sort_arr)
        for i in range(1, arr_len):
            while i > 0 and self.biger(i - 1, i):
                self.swap(i, i - 1)
                i -= 1

    def des(self):
        arr_len = len(self.sort_arr)
        for i in range(1, arr_len):
            while i > 0 and self.less(i - 1, i):
                self.swap(i, i - 1)
                i -= 1
