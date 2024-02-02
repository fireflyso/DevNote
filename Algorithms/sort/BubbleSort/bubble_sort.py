from Algorithms.sort.base.base import Base


class BubbleSort(Base):

    def __init__(self, name='冒泡'):
        super().__init__(name)

    def aes(self):
        count = len(self.sort_arr) - 1
        for i in range(count):
            have_swap = False
            for j in range(count - i):
                if self.biger(j, j + 1):
                    have_swap = True
                    self.swap(j, j + 1)
            if not have_swap:
                break
            print(self.sort_arr)

    def des(self):
        count = len(self.sort_arr) - 1
        for i in range(count):
            have_swap = False
            for j in range(count - i):
                if self.less(j, j + 1):
                    have_swap = True
                    self.swap(j, j + 1)
            if not have_swap:
                break

