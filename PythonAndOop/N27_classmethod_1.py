class MyClass:
    @classmethod
    def class_1(cls):
        print("Class method 1")

    def class_2(self):
        print("Self/Instance method 1")


if __name__ == '__main__':
    print("Calling the class `MyClass` directly without an instance:")
    MyClass.class_1()
    # MyClass.class_2()


    print("\nCalling the instance `MyClass()`:")
    MyClass().class_1()
    MyClass().class_2()