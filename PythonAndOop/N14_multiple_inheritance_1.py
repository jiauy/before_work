class A:

    def dothis(self):
        print("doing this in A")


class B(A):
    pass


class C:
    def dothis(self):
        print("doing this in C")


class D(B, C):
    pass


d_instance = D()
d_instance.dothis()  # <== This should print from class A.

print("\nPrint the Method Resolution Order")
print(D.mro())

