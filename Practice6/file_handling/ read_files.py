# ex1: read full file
with open("example.txt", "r") as f:
    print(f.read())

# ex2: read line by line
with open("example.txt", "r") as f:
    for line in f:
        print(line.strip())

# ex3: count lines
with open("example.txt", "r") as f:
    print("Lines:", len(f.readlines()))

# ex4: read first 10 characters
with open("example.txt", "r") as f:
    print(f.read(10))

# ex5: read words into list
with open("example.txt", "r") as f:
    words = f.read().split()
    print(words)