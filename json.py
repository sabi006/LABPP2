import json

#ex1
data = {"name": "Alice", "age": 25, "city": "Paris"}
json_str = json.dumps(data)
print(json_str)

# ex2
json_data = '{"fruit": "apple", "count": 5}'
py_data = json.loads(json_data)
print(py_data)

# ex3
with open("data.json", "w") as f:
    json.dump(data, f)

# ex4
with open("data.json", "r") as f:
    loaded = json.load(f)
print(loaded)

# ex5
json_array = '[{"id":1,"val":10},{"id":2,"val":20}]'
arr = json.loads(json_array)
for item in arr:
    print(item["id"], item["val"])