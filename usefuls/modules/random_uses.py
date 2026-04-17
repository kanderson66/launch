# https://docs.python.org/3/library/random.html#bookkeeping-functions

import random


# RANDOM CHOICE
# Example list of items
items = ["apple", "banana", "cherry", "date"]

# Select a single random item
selected_item = random.choice(items)

# Creates 2 random uppercase letters
letters = ''.join(random.choices(string.ascii_uppercase, k=2)) 

# Creates 3 random #s
numbers = ''.join(random.choices(string.digits, k=3)) 
# END RANDOM CHOICE

# RANDOM INT
# Generates a random integer between 1 and 6, inclusive
dice_roll = random.randint(1, 6)
print(dice_roll)
# END RANDOM INT
