t = int(input())
d = {}

for _ in range():
    parts = input().split()
    action = parts[0]
    
    if action == "set":
        key, val = parts[1], parts[2]
        doc[key] = val
    elif action == "get":
        key = parts[1]
        print(doc.get(key, f"KE: no key {key} found in the document"))

