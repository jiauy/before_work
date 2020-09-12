class A:
    def method(*argv):
        return argv

a = A()
print(a.method)