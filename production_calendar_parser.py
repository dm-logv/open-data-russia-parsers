#!/usr/bin/env python3

import argparse
import csv
from datetime import date
from sys import stdout


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', metavar='PATH', type=str, required=True,
                        dest='input', help='Input file path')
    parser.add_argument('-o', '--output', metavar='PATH', type=str,
                        dest='output', help='Output file path. Prints to STDOUT if not present')
    return parser.parse_args(args)


class ProductionCalendar:
    @classmethod
    def parse(cls, csv):
        """
        >>> data = csv.reader([
        ...     '2011,"1,2+,9,10","5","5*","2,3","22","25,26","2,3,9","21,27,28","24,25","29,30","3*","3",248,117,1981,1782.6,1187.4',
        ...     '2012,"1,2,9*,14","4+","3,4","1","12*","24,30","28,29","26","1,2,8","6,7","3,4,5","1,2",249,117,1986,1786.8,1189.2',
        ...     '2017,"1,2,12,13+","2*","2,3","6,7,13","8*,9","11*,30","27,28","3,4","1,7","5,6,12","2","31*",247,118,1970,1772.4,1179.6'])
        >>> ProductionCalendar.parse(data)
        <ProductionCalendar [<Year 2011-01-01 248 117 1981.0 1782.6 1187.4 [<Month 2011-01-01 [<Day 2011-01-01 additional_holiday=False halfday=False>, <Day 2011-01-02 additional_holiday=True halfday=False>, <Day 2011-01-09 additional_holiday=False halfday=False>, <Day 2011-01-10 additional_holiday=False halfday=False>], <Month 2011-02-01 [<Day 2011-02-05 additional_holiday=False halfday=False>], <Month 2011-03-01 [<Day 2011-03-05 additional_holiday=False halfday=True>], <Month 2011-04-01 [<Day 2011-04-02 additional_holiday=False halfday=False>, <Day 2011-04-03 additional_holiday=False halfday=False>], <Month 2011-05-01 [<Day 2011-05-22 additional_holiday=False halfday=False>], <Month 2011-06-01 [<Day 2011-06-25 additional_holiday=False halfday=False>, <Day 2011-06-26 additional_holiday=False halfday=False>], <Month 2011-07-01 [<Day 2011-07-02 additional_holiday=False halfday=False>, <Day 2011-07-03 additional_holiday=False halfday=False>, <Day 2011-07-09 additional_holiday=False halfday=False>], <Month 2011-08-01 [<Day 2011-08-21 additional_holiday=False halfday=False>, <Day 2011-08-27 additional_holiday=False halfday=False>, <Day 2011-08-28 additional_holiday=False halfday=False>], <Month 2011-09-01 [<Day 2011-09-24 additional_holiday=False halfday=False>, <Day 2011-09-25 additional_holiday=False halfday=False>], <Month 2011-10-01 [<Day 2011-10-29 additional_holiday=False halfday=False>, <Day 2011-10-30 additional_holiday=False halfday=False>], <Month 2011-11-01 [<Day 2011-11-03 additional_holiday=False halfday=True>], <Month 2011-12-01 [<Day 2011-12-03 additional_holiday=False halfday=False>]], <Year 2012-01-01 249 117 1986.0 1786.8 1189.2 [<Month 2012-01-01 [<Day 2012-01-01 additional_holiday=False halfday=False>, <Day 2012-01-02 additional_holiday=False halfday=False>, <Day 2012-01-09 additional_holiday=False halfday=True>, <Day 2012-01-14 additional_holiday=False halfday=False>], <Month 2012-02-01 [<Day 2012-02-04 additional_holiday=True halfday=False>], <Month 2012-03-01 [<Day 2012-03-03 additional_holiday=False halfday=False>, <Day 2012-03-04 additional_holiday=False halfday=False>], <Month 2012-04-01 [<Day 2012-04-01 additional_holiday=False halfday=False>], <Month 2012-05-01 [<Day 2012-05-12 additional_holiday=False halfday=True>], <Month 2012-06-01 [<Day 2012-06-24 additional_holiday=False halfday=False>, <Day 2012-06-30 additional_holiday=False halfday=False>], <Month 2012-07-01 [<Day 2012-07-28 additional_holiday=False halfday=False>, <Day 2012-07-29 additional_holiday=False halfday=False>], <Month 2012-08-01 [<Day 2012-08-26 additional_holiday=False halfday=False>], <Month 2012-09-01 [<Day 2012-09-01 additional_holiday=False halfday=False>, <Day 2012-09-02 additional_holiday=False halfday=False>, <Day 2012-09-08 additional_holiday=False halfday=False>], <Month 2012-10-01 [<Day 2012-10-06 additional_holiday=False halfday=False>, <Day 2012-10-07 additional_holiday=False halfday=False>], <Month 2012-11-01 [<Day 2012-11-03 additional_holiday=False halfday=False>, <Day 2012-11-04 additional_holiday=False halfday=False>, <Day 2012-11-05 additional_holiday=False halfday=False>], <Month 2012-12-01 [<Day 2012-12-01 additional_holiday=False halfday=False>, <Day 2012-12-02 additional_holiday=False halfday=False>]], <Year 2017-01-01 247 118 1970.0 1772.4 1179.6 [<Month 2017-01-01 [<Day 2017-01-01 additional_holiday=False halfday=False>, <Day 2017-01-02 additional_holiday=False halfday=False>, <Day 2017-01-12 additional_holiday=False halfday=False>, <Day 2017-01-13 additional_holiday=True halfday=False>], <Month 2017-02-01 [<Day 2017-02-02 additional_holiday=False halfday=True>], <Month 2017-03-01 [<Day 2017-03-02 additional_holiday=False halfday=False>, <Day 2017-03-03 additional_holiday=False halfday=False>], <Month 2017-04-01 [<Day 2017-04-06 additional_holiday=False halfday=False>, <Day 2017-04-07 additional_holiday=False halfday=False>, <Day 2017-04-13 additional_holiday=False halfday=False>], <Month 2017-05-01 [<Day 2017-05-08 additional_holiday=False halfday=True>, <Day 2017-05-09 additional_holiday=False halfday=False>], <Month 2017-06-01 [<Day 2017-06-11 additional_holiday=False halfday=True>, <Day 2017-06-30 additional_holiday=False halfday=False>], <Month 2017-07-01 [<Day 2017-07-27 additional_holiday=False halfday=False>, <Day 2017-07-28 additional_holiday=False halfday=False>], <Month 2017-08-01 [<Day 2017-08-03 additional_holiday=False halfday=False>, <Day 2017-08-04 additional_holiday=False halfday=False>], <Month 2017-09-01 [<Day 2017-09-01 additional_holiday=False halfday=False>, <Day 2017-09-07 additional_holiday=False halfday=False>], <Month 2017-10-01 [<Day 2017-10-05 additional_holiday=False halfday=False>, <Day 2017-10-06 additional_holiday=False halfday=False>, <Day 2017-10-12 additional_holiday=False halfday=False>], <Month 2017-11-01 [<Day 2017-11-02 additional_holiday=False halfday=False>], <Month 2017-12-01 [<Day 2017-12-31 additional_holiday=False halfday=True>]]]
        """
        years = []
        for data in csv:
            years.append(Year.parse(data))
        return cls(years)

    def __init__(self, years):
        self.years = years

    def __iter__(self):
        return iter(self.years)

    def __repr__(self):
        return (f'<{self.__class__.__name__}'
                f' {self.years}')


class Year:
    @classmethod
    def parse(cls, data):
        """
        >>> data = [1999, "1,3,4,6*", "6,7", "4+,26,31*", 251, 114, 2004, 1807.2, 1204.8]
        >>> Year.parse(data)
        <Year 1999-01-01 251 114 2004.0 1807.2 1204.8 [<Month 1999-01-01 [<Day 1999-01-01 additional_holiday=False halfday=False>, <Day 1999-01-03 additional_holiday=False halfday=False>, <Day 1999-01-04 additional_holiday=False halfday=False>, <Day 1999-01-06 additional_holiday=False halfday=True>], <Month 1999-02-01 [<Day 1999-02-06 additional_holiday=False halfday=False>, <Day 1999-02-07 additional_holiday=False halfday=False>], <Month 1999-03-01 [<Day 1999-03-04 additional_holiday=True halfday=False>, <Day 1999-03-26 additional_holiday=False halfday=False>, <Day 1999-03-31 additional_holiday=False halfday=True>]]
        """
        year, *months_raw, workdays, holidays, \
            work_hours_40, work_hours_36, work_hours_24 = data

        year = date(int(year), 1, 1)
        months = [Month.parse(year, i, days)
                  for i, days in enumerate(months_raw, 1)]

        return cls(year, months, int(workdays), int(holidays),
                   float(work_hours_40), float(work_hours_36), float(work_hours_24))

    def __init__(self, year, months, workdays, holidays,
                 work_hours_40, work_hours_36, work_hours_24):
        self.year = year
        self.months = months
        self.workdays = workdays
        self.holidays = holidays
        self.work_hours_40 = work_hours_40
        self.work_hours_36 = work_hours_36
        self.work_hours_24 = work_hours_24

    def __iter__(self):
        return iter(self.months)

    def __repr__(self):
        return (f'<{self.__class__.__name__} {self.year}'
                f' {self.workdays}'
                f' {self.holidays}'
                f' {self.work_hours_40}'
                f' {self.work_hours_36}'
                f' {self.work_hours_24}'
                f' {self.months}')
        

class Month:
    @classmethod
    def parse(cls, year, month_n, data):
        """
        >>> Month.parse(date(2020, 1, 1), 2, '1,3*,4+')
        <Month 2020-02-01 [<Day 2020-02-01 additional_holiday=False halfday=False>, <Day 2020-02-03 additional_holiday=False halfday=True>, <Day 2020-02-04 additional_holiday=True halfday=False>]
        """
        month = year.replace(month=month_n)
        days = [Day.parse(month, day) for day in data.split(',')]
        return cls(month, days)

    def __init__(self, month, days):
        self.month = month
        self.days = days

    def __iter__(self):
        return iter(self.days)

    def __repr__(self):
        return (f'<{self.__class__.__name__} {self.month}'
                f' {self.days}')


class Day:
    @classmethod
    def parse(cls, month, data):
        """
        >>> Day.parse(date(2020, 2, 1), '23')
        <Day 2020-02-23 additional_holiday=False halfday=False>
        >>> Day.parse(date(2020, 2, 1), '24+')
        <Day 2020-02-24 additional_holiday=True halfday=False>
        >>> Day.parse(date(2020, 4, 1), '30*')
        <Day 2020-04-30 additional_holiday=False halfday=True>
        """
        is_halfday = False
        is_additional_holiday = False

        if '*' in data:
            is_halfday = True
        if '+' in data:
            is_additional_holiday = True

        day = int(data.strip('*+'))

        return cls(month, day, is_additional_holiday, is_halfday)

    def __init__(self, month, day, is_additional_holiday, is_halfday):
        self.day = month.replace(day=day)
        self.is_additional_holiday = is_additional_holiday
        self.is_halfday = is_halfday

    def __repr__(self):
        return (f'<{self.__class__.__name__} {self.day}'
                f' additional_holiday={self.is_additional_holiday}'
                f' halfday={self.is_halfday}>')


class CalendarWriter:
    CSV_HEADER = 'dt', 'is_halfday', 'is_additional_holiday'

    def __init__(self, calendar: ProductionCalendar):
        self.calendar = calendar

    def write_csv(self, buffer):
        writer = csv.writer(buffer)
        writer.writerow(CalendarWriter.CSV_HEADER)

        days = [day
                for year in calendar
                for month in year
                for day in month]

        for day in days:
            writer.writerow([day.day, day.is_halfday,
                             day.is_additional_holiday])


if __name__ == '__main__':
    args = parse_args()

    with open(args.input, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        calendar = ProductionCalendar.parse(reader)

    if args.output:
        buffer = open(args.output, 'w', encoding='utf-8')
    else:
        buffer = stdout
    CalendarWriter(calendar).write_csv(buffer)
