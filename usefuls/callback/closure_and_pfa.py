# Closure?
def printer(message):
    print(message)

def later(func, argument):
    def inner():
        func(argument)

    return inner

print_warning = later(printer, "The system is shutting down!")
print_warning()  # The system is shutting down!

# PFA
def notify(message, when):
    print(f"{message} in {when} minutes!")

def later2(func, first_arg):
    def inner(second_arg):
        func(first_arg, second_arg)
    return inner

shutdown_warning = later2(notify, "The system is shutting down")
shutdown_warning(30) # The system is shutting down in 30 minutes!

# is PFA basically a closure that requires 1 or more extra arguments when called?
# if pass a function for a parameter in closure, is that considered a callback?