import shutil
import os

# ex1: move file
shutil.move("file.txt", "dir2/file.txt")

# ex2: move and rename
shutil.move("dir2/file.txt", "dir2/newname.txt")

# ex3: move back
shutil.move("dir2/newname.txt", "file.txt")

# ex4: move multiple files
files = ["a.txt", "b.txt"]
for f in files:
    if os.path.exists(f):
        shutil.move(f, "dir2/")

# ex5: move directory
shutil.move("dir2", "moved_dir")