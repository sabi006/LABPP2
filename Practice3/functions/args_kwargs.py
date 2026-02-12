# ex1: 
def numbers(*args):
    print(args)

numbers(1, 2, 3)


# ex2: 
def add_all(*nums):
    print(sum(nums))

add_all(1, 2, 3, 4)


# ex3:
def info(**kwargs):
    print(kwargs)

info(name="Anna", age=20)


# ex4: 
def example(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

example(1, 2, name="Tom")
