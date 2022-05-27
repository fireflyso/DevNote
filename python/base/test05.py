class A:
    def method(self):
        print("CommonA")


class B(A):
    pass


class C(A):
    def method(self):
        print("CommonC")


class D(B, C):
    pass


print("test : {}".format(D().method()))
print(D.__mro__)
