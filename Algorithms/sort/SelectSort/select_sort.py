# -*- coding: utf-8 -*-

import sys,os
srcpath = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
sys.path.append(srcpath)

from Algorithms.sort.base.base import Base

class SelectSort(Base):

    def __init__(self,name = "选择"):
        super().__init__(name)

    def aes(self):
        for i in range(len(self.sort_arr)):
            for j in range(i+1,len(self.sort_arr)):
                if(self.biger(i,j)):
                    self.swap(i,j)

    def des(self):
        for i in range(len(self.sort_arr)):
            for j in range(i+1,len(self.sort_arr)):
                if(self.less(i,j)):
                    self.swap(i,j)
