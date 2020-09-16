class PrintList(object):

    def __init__(self, my_list):
        self.mylist = my_list

    def __repr__(self):
        return str(self.mylist)


if __name__ == '__main__':
    printlist = PrintList(["a", "b", "c"])
    print(printlist.__repr__())
    print(printlist)