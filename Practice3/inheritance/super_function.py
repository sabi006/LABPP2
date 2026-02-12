# ex1: 
class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        super().greet()
        print("I am a student")

s = Student()
s.greet()


# ex2: 
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

d = Dog("Rex")
print(d.name)


# ex3:
class Employee:
    def __init__(self, name):
        self.name = name

class Manager(Employee):
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary

m = Manager("Ali", 5000)
print(m.name, m.salary)


# ex4:
class Parent:
    def show(self):
        print("Parent method")

class Child(Parent):
    def show(self):
        super().show()
        print("Child method")

c = Child()
c.show()
