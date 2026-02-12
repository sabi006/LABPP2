# ex1:
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()


# ex2: 
class Cat(Animal):
    pass

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
    pass

f1 = Fish()
f2 = Fish()
f1.speak()
f2.speak()
