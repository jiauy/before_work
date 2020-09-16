class Date:
    def get_date(self,date):
        print("2016-05-14")
        return date


class Time(Date):
    def get_time(self,time):
        print("07:00:00")
        return time

if __name__ == '__main__':
    dt = Date()
    dt.get_date()
    print("--------")

    tm = Time()
    tm.get_time()

    tm.get_date()