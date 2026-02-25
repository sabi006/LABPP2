#ex1
class A:
    def hello(self):
        print("Hello from A")

class B:
    def hi(self):
        print("Hi from B")

class C(A, B):
    pass

c = C()
c.hello()
c.hi()


print("------")

#ex2
class A:
    def greet(self):
        print("A greet")

class B:
    def greet(self):
        print("B greet")

class C(A, B):
    pass

c = C()
c.greet()   # A greet


print("------")

#ex3
print(C.__mro__)


print("------")

#ex4
class A:
    def greet1(self):
        print("Hello from A")

class B:
    def greet2(self):
        print("Hello from B")

class C(A, B):
    def greet(self):
        print("Hello from C")

c = C()
c.greet1()
c.greet2()

