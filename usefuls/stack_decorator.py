# explanation at bottom
def dec1(dec2):
    def inner(*args, **kwargs):
        print('First decorator')
        dec2(*args, **kwargs)
        print('leave1')
        return
    return inner

def dec2(func):
    def inner(*args, **kwargs):
        print('Second decorator')
        func(*args, **kwargs)
        print('leave2')
        return
    return inner

@dec1
@dec2
def add_dec(x, y):
    print(x + y)

add_dec(1, 2)


def add(x, y):
    print(x + y)

print('\nEquivalent to:')
decorated = dec1(dec2(add))
decorated(1, 2)

""" Breakdown:
- Pass 'add' function into dec2 as argument
- dec2 returns inner function to dec1 as PFA with 'add' saved
- dec1 receives dec2's inner function as its parameter
- dec1 returns its own inner function to 'decorated' variable as PFA with dec2's inner function saved
- When call 'decorated', pass in 2 args, starts executing dec1's inner function first, steps through code to all funcs
"""
