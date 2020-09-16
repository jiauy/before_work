def honirific(cls):
    class HonirificCls(cls):
        def full_name(self):
            return "Dr. " + super(HonirificCls, self).full_name()

    return HonirificCls


@honirific
class Name:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self):
        return " ".join([self.first_name, self.last_name])

if __name__ == '__main__':
    result = Name("Vimal", "A.R").full_name()
    print("Full name: {0}".format(result))
