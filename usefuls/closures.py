foo0 = 5

def bar1():
    foo1 = 2
    foo2 = 3

    def bar2():
        foo3 = 4
        print(foo0)     # doesnt create closure (global)
        print(foo1)   # creates closure (nonlocal)
        print(foo2)   # creates closure (nonlocal)
        print(foo3)     # doesnt create closure (local)
        return 'hi'

    return bar2

def main():
    example = bar1()
    foo0 = 1
    print(example.__closure__)
    print(example())

if __name__ == "__main__":
    main()
    