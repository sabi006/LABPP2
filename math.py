import math
import random

# ex1
nums = [-5, 2, 7, -1]
print(min(nums), max(nums), abs(-10), round(3.6), pow(2, 3))

# ex2
print(math.sqrt(16), math.ceil(2.3), math.floor(2.7), math.pi)

# ex3
angle = math.pi / 4
print(math.sin(angle), math.cos(angle))

# ex4
print(random.randint(1, 10))
print(random.choice(['a', 'b', 'c']))

# ex5
items = [1, 2, 3, 4, 5]
random.shuffle(items)
print(items)