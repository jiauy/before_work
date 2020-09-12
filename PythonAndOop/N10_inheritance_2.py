class Animal():
    def __init__(self, name):
        self.name = name

    def eat(self, food):
        print("%s is eating %s" % (self.name, food))


class Dog(Animal):
    def fetch(self, thing):
        print("%s goes after the %s" % (self.name, thing))


class Cat(Animal):
    def swatstring(self):
        print("%s shred the string!" % self.name)


d = Dog("Roger")
c = Cat("Fluffy")

d.fetch("paper")
d.eat("dog food")
print("--------")
c.eat("cat food")
c.swatstring()

c.fetch("frizbee")
d.swatstring()
