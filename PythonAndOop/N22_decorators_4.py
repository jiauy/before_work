def decorator(inner):
    def inner_decorator(*args, **kwargs):
        print(args, kwargs)
    return inner_decorator


@decorator
def decorated(string_args):
    print("This happened : " + string_args)

if __name__ == "__main__":
    decorated("Hello, how are you?","i m fine")
#装饰器不调用被修饰函数,就能够使的被修饰函数与原函数无关了
