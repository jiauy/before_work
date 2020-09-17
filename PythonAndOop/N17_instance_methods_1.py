class A:
    def method(*args):#中途发现 这个类与一般的不同,没有self,目的就是为了显示地址
        return args

if __name__ == '__main__':
    a = A()
    result = a.method([1,2,3,4])
    print(result)