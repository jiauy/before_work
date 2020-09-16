class A:
    def method(*argv):
        return argv

if __name__ == '__main__':
    a = A()
    print(a.method)