# ex1: write text
with open("file.txt", "w") as f:
    f.write("Hello World\n")

# ex2: append text
with open("file.txt", "a") as f:
    f.write("Appended line\n")

# ex3: write list to file
data = ["A", "B", "C"]
with open("file.txt", "w") as f:
    for item in data:
        f.write(item + "\n")

# ex4: write numbers
with open("nums.txt", "w") as f:
    for i in range(5):
        f.write(str(i) + "\n")

# ex5: copy content manually
with open("file.txt", "r") as f1, open("copy.txt", "w") as f2:
    f2.write(f1.read())