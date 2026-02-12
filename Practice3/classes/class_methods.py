# ex1: 
class Person:
    def say_hello(self):
        print("Hello")

p = Person()
p.say_hello()


# ex2: 
class School:
    name = "ABC School"


    def show_name(cls):
        print(cls.name)

School.show_name()


# ex3: 
class Math:

    def add(a, b):
        return a + b

print(Math.add(2, 3))


# ex4:
class Example:
    number = 10

    def __init__(self, value):
        self.value = value

    def show_value(self):
        print(self.value)


    def show_number(cls):
        print(cls.number)

    def greet():
        print("Hi!")

e = Example(5)
e.show_value()
Example.show_number()
Example.greet()

