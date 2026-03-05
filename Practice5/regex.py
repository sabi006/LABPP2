#1.Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re
text = "abbbb"
pattern = r"ab*"
if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")

#2.Python program that matches a string that has an 'a' followed by two to three 'b'.
import re
text = "abbb"
pattern = r"ab{2,3}"
if re.fullmatch(pattern, text):
    print("Match")

#3.Python program to find sequences of lowercase letters joined with a underscore.
import re
text = "hello_world"
pattern = r"[a-z]+_[a-z]+"
print(re.findall(pattern, text))

#4.Python program to find the sequences of one upper case letter followed by lower case letters.
import re
text = "Hello World Python"
print(re.findall(r"[A-Z][a-z]+", text))

#5.Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
import re
text = "axyzbc"
pattern = r"^a.*b$"
if re.search(pattern, text):
    print("Match")
else:
    print("No Match")


#6.Python program to replace all occurrences of space, comma, or dot with a colon.
import re
text = "Python, Java. C++"
result = re.sub(r"[ ,\.]", ":", text)
print(result)

#7.python program to convert snake case string to camel case string.
import re
text = "hello_world_test"
result = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)
print(result)

#8.Python program to split a string at uppercase letters.
import re
text = "HelloWorldPython"
words = re.split(r"(?=[A-Z])", text)
print(words)

#9.Python program to insert spaces between words starting with capital letters.
import re
text = "HelloWorldPython"
result = re.sub(r"([A-Z])", r" \1", text).strip()
print(result)

#10.Python program to convert a given camel case string to snake case.
import re
text = "helloWorldTest"
result = re.sub(r"([A-Z])", r"_\1", text).lower()
print(result)