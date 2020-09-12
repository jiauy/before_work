import datetime


def my_decorator(inner):
    def inner_decorator():
        print(datetime.datetime.utcnow())
        inner()
        print(datetime.datetime.utcnow())
    return inner_decorator


@my_decorator
def decorated():
    print("This happened!")

if __name__ == "__main__":
    decorated()