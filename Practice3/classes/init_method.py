# ex1: 
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Anna")
print(p.name)


# ex2: 
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s = Student("Ali", 20)
print(s.name)
print(s.age)


# ex3:
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print(self.name, "says Woof")

d = Dog("Rex")
d.bark()


# ex4:
class Car:
    def __init__(self, brand="Toyota"):
        self.brand = brand

c1 = Car()
c2 = Car("Honda")

print(c1.brand)
print(c2.brand)
