# ex1:
numbers = [1, 2, 3, 4, 5]
result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)


# ex2: 
numbers = [1, 2, 3, 4, 5]
result = list(filter(lambda x: x % 2 != 0, numbers))
print(result)


# ex3:
numbers = [1, 2, 3, 4, 5]
result = list(filter(lambda x: x > 3, numbers))
print(result)


# ex4:
numbers = [-2, -1, 0, 1, 2]
result = list(filter(lambda x: x > 0, numbers))
print(result)
