import sys,os
srcpath = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(srcpath)

from base.base import Base

class SelectSort(Base):

    def sort_aes(self):
        for i in range(len(self.sort_arr)):
            for j in range(i+1,len(self.sort_arr)):
                if(self.sort_arr[i] > self.sort_arr[j]):
                    self.swap(i,j)

    def sort_des(self):
        for i in range(len(self.sort_arr)):
            for j in range(i+1,len(self.sort_arr)):
                if(self.sort_arr[i] < self.sort_arr[j]):
                    self.swap(i,j)
    
ss = SelectSort()
# ss.sort_aes()
ss.sort_des()
print(ss.sort_arr)