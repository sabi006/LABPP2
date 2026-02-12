# ex1: 
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof")

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
    def speak(self):
        super().speak()
        print("Chirp")

b = Bird()
b.speak()


# ex4: 
class Fish(Animal):
    def speak(self):
        print("Blub")

f = Fish()
f.speak()
