#ex1

print(bool("Hello"))
print(bool(15))
#ex2
x = "Hello"
y = 15
print(bool(x))
print(bool(y))

#ex3
print(bool("abc"))
print(bool(123))
print(bool(["apple", "cherry", "banana"]))

#ex4
print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

#ex5
class MyClass:
    def __len__(self):
        return 0

myobj = MyClass()
print(bool(myobj))
