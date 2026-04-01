"""
A function that often appears in languages that have map and filter functions 
is called the reduce function, or, sometimes, inject. 
Python has one tucked away in the functools module, but we won't be using it in this challenge.

The reduce function reduces the elements in an iterable object to a single value. 
For instance, reduce can return the sum of all numbers in a list or concatenate 
the strings in a tuple to form a single long string. 
It's a bit like map, but instead of returning a new collection, it just returns a single value.

reduce functions typically take 3 arguments:

1. A callback that takes two arguments. 
The first argument is the current element of the iterable argument and 
the second is the current reduction value, commonly called the "accumulator" and named accum.
2. An iterable.
3. A starting value. The starting value is the initial value for the current argument in the callback.

For instance, consider the following reduce invocation:

numbers = [10, 3, 5]
product = lambda number, accum: accum * number
print(reduce(product, numbers, 2))     # 300

On the first invocation of the product lambda, number will be 10 while accum will be 2, 
the starting value given by the third argument to reduce. The callback will return 20.

On the second invocation of product, number will be 3 while accum will be 20, 
the return value from the previous invocation. The return value will be 60.

On the final invocation, number will be 5, accum will be 60, and the return value will be 300.

reduce always uses the callback like this. 
The first invocation gets passed the first element of the iterable and the starting value given by reduce's third argument. 
It then passes the callback the second element of the iterable and the return value of the first invocation. 
This continues until all elements have been processed by the callback, 
and the final return value of reduce is the return value of the last callback invocation.

Your job in this problem is to implement reduce. Beware: this may be a challenging problem. 
We recommend not using comprehensions.

Question 4
Use the reduce function shown in the answer to the previous question to compute the sum of the squares in a list of numbers.
"""
def reduce(callback, iterable, accum):
    for item in iterable:
        accum = callback(item, accum)
    return accum

def test2():
    nums = [1, 2, 3]
    sum_squares = lambda num, accum: accum + num**2
    print(reduce(sum_squares, nums, 0))

test2()

# def test1():
#     numbers = (1, 2, 4, 8, 16)
#     total = lambda number, accum: accum + number
#     print(reduce(total, numbers, 0))        # 31

#     numbers = [10, 3, 5]
#     product = lambda number, accum: accum * number
#     print(reduce(product, numbers, 2))      # 300

#     colors = ['red', 'orange', 'yellow', 'green',
#             'blue', 'indigo', 'violet']
#     rainbow = lambda color, accum: accum + color[0].upper()
#     print(reduce(rainbow, colors, ''))      # ROYGBIV
# test1()

