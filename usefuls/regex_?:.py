import re

text = ("A grey cat\n" +
    "A blue caterpillar\n" +
    "The lazy dog\n" +
    "The white cat\n" +
    "A loud dog\n" +
    "--A loud dog\n" +
    "Go away dog\n" +
    "The ugly rat\n" +
    "The lazy, loud dog")

# no ?:
print(re.findall(r"^(A|The) [a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z] (dog|cat)$", text, flags=re.M))

# with ?:
print(re.findall(r"^(?:A|The) [a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z] (?:dog|cat)$", text, flags=re.M))
