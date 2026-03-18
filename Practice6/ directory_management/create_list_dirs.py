import os

# ex1: create directory
os.mkdir("dir1")

# ex2: create nested directory
os.makedirs("dir2/subdir", exist_ok=True)

# ex3: list files
print(os.listdir())

# ex4: check if directory exists
print(os.path.isdir("dir1"))

# ex5: remove directory
os.rmdir("dir1")