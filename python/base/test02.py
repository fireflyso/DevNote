#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Student:
    name = 'globe_name'

    def __init__(self):
        self.name = 'name'


s1 = Student()
print(s1.name)  # name  实例属性优先级更高，先找实例属性，没有才会找类属性


