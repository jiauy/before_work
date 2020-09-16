class MyList(list):

    def __getitem__(self, index):
        if index == 0:
            raise IndexError
        if index > 0:
            index -= 1
        return list.__getitem__(self, index)

    def __setitem__(self, index, value):
        if index == 0:
            raise IndexError
        if index > 0:
            index -= 1
        list.__setitem__(self, index, value)


if __name__ == '__main__':
    x = MyList(['a', 'b', 'c'])
    print(x)
    print("-" * 10)

    x.append('d')
    print(x)
    print("-" * 10)

    x.__setitem__(4, 'e')
    print(x)
    print("-" * 10)

    print(x[1])
    print(x.__getitem__(1))
    print("-" * 10)

    print(x[4])
    print(x.__getitem__(4))