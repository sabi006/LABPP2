#ex1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
#ex2
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)
#ex3
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")