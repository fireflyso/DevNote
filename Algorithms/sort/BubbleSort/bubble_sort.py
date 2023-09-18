import sys, os

srcpath = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
sys.path.append(srcpath)

from Algorithms.sort.base.base import Base


class BubbleSort(Base):

    def __init__(self, name='冒泡'):
        super().__init__(name)

    def aes(self):
        for _ in range(len(self.sort_arr)):
            for j in range(len(self.sort_arr) - 1):
                if (self.biger(j, j + 1)):
                    self.swap(j, j + 1)

    def des(self):
        for _ in range(len(self.sort_arr)):
            for j in range(len(self.sort_arr) - 1):
                if (self.less(j, j + 1)):
                    self.swap(j, j + 1)
