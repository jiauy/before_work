class Date():
    def get_date(self):
        print("2016-05-14")


class Time(Date):
    def get_time(self):
        print("07:00:00")


dt = Date()
dt.get_date()
print("--------")

tm = Time()
tm.get_time()

tm.get_date()