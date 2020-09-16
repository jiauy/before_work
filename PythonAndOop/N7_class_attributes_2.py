class YourClass:
    classy = "class value"
    # def x(self):
    #     return

if __name__ == '__main__':
    print(YourClass.classy)
    dd = YourClass()
    print(dd.classy)

    dd.classy = "Instance value"
    print(dd.classy)

    del dd.classy

    print(dd.classy)
#理解实例对象的内容,需要调用才能够生成,直接删除是不可以的,因为还没生成.不能直接获取.