# coding:utf-8
# @Time : 2023/3/13 22:37
# @Author : Andy.Zhang
# @Desc : python_trainning 3.X

"""
Question

Given a specific date, write a function to return the day of the year for that date. The signature of the function is
         int dayOfYear(int year, int month, int day)

For example, given input of year=2016, month=1, day=3.
    The function should return 3 as the date 2016-01-03 is the 3rd day of the year 2016.

Another example, given input of year=2016, month=2, day=1.
    The function should return 32 as the date 2016-02-01 is the 32nd day of the year 2016.

Notes:
Please return -1 for invalid input.
Please write your own algorithm. Do NOT use any class like Calendar in Java.
Please give a full implementation. Do NOT write pseudo code.
Please include your own logic of determining a leap year.
You are free to choose any programming language, not limited to Java, C# or C++.
    Please tell us the programming language you used in your answer.
"""


def get_days_from_date(year: int, month: int, day: int) -> int:
    # validating the parameters
    if year < 1970 or month < 1 or month > 12 or day < 1 or day > 31:
        return -1  # invalid input
    else:
        # checking the day is out of range for month
        if month == 2:
            # day can not be larger than 29 in the leap year
            if year % 400 == 0 or year % 4 == 0 and year % 100:
                if day > 29:
                    return -1
            else:
                # day can not be larger than 28 in the normal year
                if day > 28:
                    return -1
        elif month not in (1, 3, 5, 7, 8, 10, 12) and day > 30:
            # day can not be larger than 30
            return -1

    # kernel logic code
    days = 0

    month -= 1
    while month:
        if month in (1, 3, 5, 7, 8, 10, 12):
            days += 31
        elif month == 2:
            # if not year % 400 or not year % 4 and year % 100:
            if year % 400 == 0 or year % 4 == 0 and year % 100:
                # find a leap year
                days += 29
            else:
                days += 28
        else:
            days += 30  # month in (2, 4, 6, 9, 11)

        month -= 1
    else:
        days += day

    return days


def test_answer(max_test_times: int = 10000) -> None:
    import random
    import datetime as dt

    def get_days(year: int, month: int, day: int) -> int:
        date = dt.date(year, month, day)
        days = date.strftime('%j')
        return int(days)

    max_test_times = max_test_times if max_test_times else 10000
    failed = 0
    for i in range(max_test_times):
        print('testing times:{0}, successfully rate:{1}%'.format(i+1, int((max_test_times-failed)/max_test_times*100)))
        year = random.randint(1970, 9999)
        month = random.randint(1, 12)  # 1 <= month <= 12
        day = random.randint(1, 31)  # 1 <= day <= 31

        _ = get_days_from_date(year, month, day)
        if _ != -1:
            if _ != get_days(year, month, day):
                failed += 1
        else:
            print("invalid date for {0}-{1}-{2}".format(year, month, day))


if __name__ == "__main__":
    print('\n ----------------unit testing automatic----------------')
    test_answer(max_test_times=5000)  # just adjust this parameter if it needs more testing.

    print('\n ----------------testing step by step----------------')
    print(get_days_from_date(2016, 1, 3))
    print(get_days_from_date(2016, 2, 1))

    print(get_days_from_date(2016, 3, 1))
    print(get_days_from_date(2023, 3, 1))
    print(get_days_from_date(2016, 4, 31))  # 2016-4-31 was a wrong date, should be return -1

    print(get_days_from_date(2016, 2, 29))
    print(get_days_from_date(2023, 2, 29))  # 2023-2-29 was a wrong date, should be return -1

