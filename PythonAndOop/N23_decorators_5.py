from __future__ import print_function


# 2. Decorator function
def handle_exceptions(func_name):
    def inner(*args, **kwargs):
        try:
            return func_name(*args, **kwargs)
        except Exception:
            print("An exception was thrown : ", Exception)
    return inner


# 1. Main function
@handle_exceptions
def divide(x, y):
    return x / y


if __name__ == '__main__':
    print(divide(8, 0))