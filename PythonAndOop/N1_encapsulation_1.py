#封装练习
#没必要，默认继承object。
class MyClass:
    def set_val(self,val):
        self.value = val

    def get_val(self):
        print(self.value)
        return self.value

