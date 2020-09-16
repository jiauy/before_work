class MyClass:
    def set_val(self,val):
        self.value = val

    def get_val(self):
        print(self.value)
        return self.value

if __name__ == '__main__':
    a=MyClass()
    a.set_val(5)
    print(a.value)