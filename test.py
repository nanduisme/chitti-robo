import inspect

def dec(f):
    def wrapper(a, b):
        f(a*2, b)
    return wrapper

@dec
def add(a, b):
    print(a + b)

print(add(1, 1))