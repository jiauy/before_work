class PrintList:

    def __init__(self, my_list):
        self.mylist = my_list

    def __repr__(self):
        return str(self.mylist)


if __name__ == '__main__':
    # printlist = PrintList([1,2,3])
    # print(printlist.__repr__())
    # print(printlist.mylist)
    # print(printlist==printlist.__repr__())
    print('[1]'=='[1]')