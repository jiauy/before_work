
class MyInteger:
    def set_val(self, val):
        try:
            val = int(val)
        except ValueError:
            return
        self.val = val

    def get_val(self):
        print(self.val)

    def increment_val(self):
        self.val = self.val + 1
        print(self.val)
if __name__ == '__main__':
    a=MyInteger()
    a.get_val()