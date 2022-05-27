
class Student:
    # 类属性
    count = 0

    def __init__(self, name) -> None:
        # 实例属性
        self.name = name
        Student.count += 1


for i in range(10):
    s = Student(i)
    print('name : {}, count : {}'.format(s.name, s.count))



