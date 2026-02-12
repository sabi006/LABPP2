# ex1: 
class Animal:
    def speak(self):
        print("Sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()


# ex2: 
class Cat(Animal):
    def speak(self):
        print("Meow")

c = Cat()
c.speak()


# ex3: 
class Bird(Animal):
    def fly(self):
        print("Flying")

b = Bird()
b.speak()
b.fly()


# ex4: 
class Fish(Animal):
    def swim(self):
        print("Swimming")

f = Fish()
f.swim()
