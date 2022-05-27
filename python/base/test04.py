COUNT = 1

class Student:
    name = 'globe_name'

    def __init__(self):
        self.age = 100

    def instence_foo(self):
        print('instence_foo')
        print('get COUNT : {}'.format(COUNT))
        print('get name : {}'.format(self.name))
        print('get age : {}'.format(self.age))

    @classmethod
    def class_test(cls):
        print('class_test')

    @classmethod
    def class_foo(cls):
        print('class_foo')
        print('get COUNT : {}'.format(COUNT))
        print('get name : {}'.format(cls.name))
        cls.class_test()
        # print('get age : {}'.format(cls.age))   # AttributeError: type object 'Student' has no attribute 'age'

    @staticmethod
    def static_foo():
        print('static_foo')
        print('get COUNT : {}'.format(COUNT))


s1 = Student()
s1.static_foo()
s1.class_foo()
s1.static_foo()
