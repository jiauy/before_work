class InstanceCounter:
    count = 0

    def __init__(self, val):
        self.val = val
        InstanceCounter.count += 1

    def set_val(self, newval):
        self.val = newval

    def get_val(self):
        print(self.val)

    def get_count(self):
        print(InstanceCounter.count)

# a = InstanceCounter(5)
# a = InstanceCounter()
# b = InstanceCounter(10)
# c = InstanceCounter(15)
# InstanceCounter.count=5
if __name__ == '__main__':
    #print(a.count1)

    # a.count1='asdf'
    # print(InstanceCounter.count1)
    # del a.count1
    # for obj in (a, b, c):
    #     print("value of obj: %s" % obj.get_val())
    #     print("Count : %s" % obj.get_count())
    #
    # print(InstanceCounter.count)
    print(InstanceCounter.count1)