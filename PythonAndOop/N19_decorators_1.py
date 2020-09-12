def my_decorator(my_function):
    def inner_decorator():
        print("This happened before!")
        my_function()
        print("This happens after ")
        print("This happened at the end!")
    return inner_decorator



@my_decorator
def my_decorated():
    print("This happened!")

if __name__ == '__main__':
    my_decorated()