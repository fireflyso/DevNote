
class Student:
    # 类属性
    __count = 0

    def __init__(self, name) -> None:
        # 实例属性
        self.name = name
        Student.__count += 1
        self.__age = 100
        self._score = 1000


s1 = Student('haha')
print(s1._score)    # 1000
# print(s1.__age)     # AttributeError: 'Student' object has no attribute '__age'
print(dir(s1))      # ['_Student__age', '_Student__count', '__class__', ... 'name']
print('age : {}, count: {}'.format(s1._Student__age, s1._Student__count))   # age : 100, count: 1

for i in range(5):
    s = Student(i)
    print('name : {}, count : {}'.format(s.name, s._Student__count))

