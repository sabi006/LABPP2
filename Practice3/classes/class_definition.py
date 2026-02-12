# ex1:
class Student:
    def __init__(self, name):
        self.name = name

s1 = Student("Anna")
print(s1.name)


# ex2: 
class Book:
    def __init__(self, title):
        self.title = title

b1 = Book("Math")
b2 = Book("English")
print(b1.title)
print(b2.title)


# ex3:
class Dog:
    def bark(self):
        print("Woof")

d = Dog()
d.bark()


# ex4:
class Car:
    wheels = 4   # class variable

c1 = Car()
c2 = Car()
print(c1.wheels)
print(c2.wheels)


