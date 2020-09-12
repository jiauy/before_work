class A:

    def dothat(self):
        print("Doing this in A")


class B(A):
    pass


class C:

    def dothis(self):
        print("\nDoing this in C")


class D(B, C):
    """Multiple Inheritance,
    D inheriting from both B and C"""
    pass

d_instance = D()

d_instance.dothis()

print("\nPrint the Method Resolution Order")
print(D.mro())