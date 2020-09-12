import datetime


def my_decorator(inner):
    def inner_decorator(num_copy):
        print(datetime.datetime.utcnow())
        inner(int(num_copy) + 1)
        print(datetime.datetime.utcnow())
    return inner_decorator


@my_decorator
def decorated(number):
    print("This happened : " + str(number))

if __name__ == "__main__":
    decorated(5)