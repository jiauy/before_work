class MyClass:
    def set_val(self, val):
        self.value = val

    def get_val(self):
        print(self.value)

if __name__ == '__main__':
    a = MyClass()
    b = MyClass()

    a.set_val(10)
    b.set_val(1000)
    a.value = 100

    a.get_val()
    b.get_val()
