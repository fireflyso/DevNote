import sys,os
srcpath = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
sys.path.append(srcpath)

from Algorithms.sort.SelectSort.select_sort import SelectSort
from Algorithms.sort.BubbleSort.bubble_sort import BubbleSort
from Algorithms.sort.InsertSort.insert_sort import InsertSort

class Run:

    def select_sort(self):
        ss = SelectSort()
        ss.sort_aes()
        ss.sort_des()

    def bubble_sort(self):
        bs = BubbleSort()
        bs.sort_aes()
        bs.sort_des()

    def insert_sort(self):
        iss = InsertSort()
        iss.sort_aes()
        iss.sort_des()


if __name__ == '__main__':
    run = Run()
    # run.select_sort()
    # run.bubble_sort()
    run.insert_sort()