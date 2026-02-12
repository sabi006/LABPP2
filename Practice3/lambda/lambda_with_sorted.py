# ex1:
numbers = [5, 2, 8, 1]
result = sorted(numbers, key=lambda x: x)
print(result)


# ex2: 
numbers = [5, 2, 8, 1]
result = sorted(numbers, key=lambda x: x, reverse=True)
print(result)


# ex3:
words = ["apple", "kiwi", "banana"]
result = sorted(words, key=lambda x: len(x))
print(result)


# ex4: 
words = ["cat", "dog", "apple"]
result = sorted(words, key=lambda x: x[-1])
print(result)
