from functools import reduce

nums = [1, 2, 3, 4, 5]

# ex1: map (square)
print(list(map(lambda x: x**2, nums)))

# ex2: map (to string)
print(list(map(str, nums)))

# ex3: filter (even)
print(list(filter(lambda x: x % 2 == 0, nums)))

# ex4: filter (>3)
print(list(filter(lambda x: x > 3, nums)))

# ex5: reduce (sum)
print(reduce(lambda x, y: x + y, nums))