import shutil
import os

# ex1: copy file
shutil.copy("file.txt", "copy.txt")

# ex2: copy with new name
shutil.copy("file.txt", "new_copy.txt")

# ex3: check existence
print(os.path.exists("file.txt"))

# ex4: delete file
if os.path.exists("copy.txt"):
    os.remove("copy.txt")

# ex5: rename file
os.rename("new_copy.txt", "renamed.txt")