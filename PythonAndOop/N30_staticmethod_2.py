class MyClass:
    count = 0

    def __init__(self, name):
        print("An instance is created!")
        self.name = name
        MyClass.count += 1

    @staticmethod
    def status():
        print("The total number of instances are ", MyClass.count)

print(MyClass.count)

my_func_1 = MyClass("MyClass 1")
my_func_2 = MyClass("MyClass 2")
my_func_3 = MyClass("MyClass 3")

MyClass.status()
print(MyClass.count)