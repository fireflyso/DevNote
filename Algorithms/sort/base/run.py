from Algorithms.sort.QuickSort import QuickSort
from Algorithms.sort.SelectSort.select_sort import SelectSort
from Algorithms.sort.BubbleSort.bubble_sort import BubbleSort
from Algorithms.sort.InsertSort.insert_sort import InsertSort


def select_sort():
    ss = SelectSort()
    ss.sort_aes()
    ss.sort_des()


def bubble_sort():
    bs = BubbleSort()
    bs.sort_aes()
    bs.sort_des()


def insert_sort():
    iss = InsertSort()
    iss.sort_aes()
    iss.sort_des()


def quick_sort():
    qs = QuickSort()
    qs.sort_aes()
    # qs.sort_des()


if __name__ == '__main__':
    # select_sort()
    # bubble_sort()
    # insert_sort()
    quick_sort()
