import sys,os
srcpath = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
sys.path.append(srcpath)

from Algorithms.sort.SelectSort.select_sort import SelectSort

class Run:

    def select_sort(self):
        ss = SelectSort()
        ss.sort_aes()
        ss.sort_des()


if __name__ == '__main__':
    run = Run()
    run.select_sort()
