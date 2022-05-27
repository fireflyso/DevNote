from types import MethodType


class Student:
    pass


s = Student()
s.name = 'test'
print(s.name)   # test


def set_name(self, name):
    self.name = name


s.set_name = MethodType(set_name, s)    # 为对象绑定方法，只有该对象可以使用
s.set_name('haha')
print(s.name)   # haha

# s1 = Student()
# s1.set_name('s1')
#  'Student' object has no attribute 'set_name'  这个实例没有绑定该方法

Student.set_name = set_name     # 为class绑定方法，所有的对象都可以使用
s2 = Student()
s2.set_name('s2')
print(s2.name)  # s2


class Teacher:
    __slots__ = ('name', 'age', 'set_name')    # 通过这个方法可以预留一些属性，同时也是限制
    # TODO 那和直接定义相应的实例属性有什么区别


t1 = Teacher()
t1.name = '老师'
t1.age = 25
print('name : {}, age : {}'.format(t1.name, t1.age))    # name : 老师, age : 25
# t1.score = 100    score属性无法被绑定
# t1.set_name = set_name
# t1.set_name(name='new name')
# print('name : {}, age : {}'.format(t1.name, t1.age))
# TODO 同样不能绑定成功

