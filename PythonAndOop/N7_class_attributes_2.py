class YourClass:
    classy = "class value"
    # def x(self):
    #     return


dd = YourClass()
print(dd.classy)

dd.classy = "Instance value"
print(dd.classy)

del dd.classy

print(dd.classy)