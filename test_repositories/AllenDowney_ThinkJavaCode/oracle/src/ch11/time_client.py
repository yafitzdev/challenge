"""Class that uses Time objects (port of ch11/TimeClient.java)."""
from .time import Time


class TimeClient:

    @staticmethod
    def main(args):
        time = Time(11, 59, 59.9)
        print(time)

        s = str(time)
        print(s)

        time1 = Time(9, 30, 0.0)
        time2 = time1
        time3 = Time(9, 30, 0.0)

        print(str(time1 is time2).lower())
        print(str(time1 is time3).lower())
        print(str(time1.equals(time2)).lower())
        print(str(time1.equals(time3)).lower())

        start_time = Time(18, 50, 0.0)
        running_time = Time(2, 16, 0.0)
        end_time = Time.add(start_time, running_time)

        # using the instance method
        end_time = start_time.add(running_time)
