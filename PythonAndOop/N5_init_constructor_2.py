class MyNum():
    def __init__(self, value):
        try:
            value = int(value)
        except ValueError:
            value = 0
        self.value = value

    def increment(self):
        self.value = self.value + 1
        print(self.value)

if __name__ == '__main__':
    a = MyNum(10)
    a.increment()
    a.increment()