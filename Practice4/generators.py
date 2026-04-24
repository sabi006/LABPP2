#ex1
nums = iter([1, 2, 3, 4, 5])
for n in nums:
    print(n)

#ex2
class Count:
    def __init__(self, limit):
        self.n = 0
        self.limit = limit
    def __iter__(self):
        return self
    def __next__(self):
        if self.n < self.limit:
            self.n += 1
            return self.n
        else:
            raise StopIteration
for i in Count(5):
    print(i)

#ex3
def squares(n):
    for i in range(1, n+1):
        yield i*i
for val in squares(5):
    print(val)

# ex4
cubes = (x**3 for x in range(1, 6))
for val in cubes:
    print(val)

# ex5
def multiples_of_seven():
    n = 7
    while n <= 100:
        yield n
        n += 7
for val in multiples_of_seven():
    print(val)