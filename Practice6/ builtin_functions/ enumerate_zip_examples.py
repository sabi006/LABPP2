names = ["A", "B", "C"]
scores = [10, 20, 30]

# ex1: enumerate basic
for i, v in enumerate(names):
    print(i, v)

# ex2: enumerate with start
for i, v in enumerate(names, 1):
    print(i, v)

# ex3: zip lists
for n, s in zip(names, scores):
    print(n, s)

# ex4: zip to dict
print(dict(zip(names, scores)))

# ex5: unzip
pairs = list(zip(names, scores))
n, s = zip(*pairs)
print(n, s)