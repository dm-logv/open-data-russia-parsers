# Open Data Russia Parsers

Parsers for strange CSV from https://data.gov.ru/ into the simple Python objects.


# Parsers

## Production Calendar

Provides parser and class structure for CSV on the https://data.gov.ru/opendata/7708660670-proizvcalendar page.

> Download datasets from link above to run examples.


### Usage

- Parse a CSV dataset and print a result:

    ```sh
    $ ./production_calendar_parser.py -i data-sample.csv
    dt,is_halfday,is_additional_holiday
    1999-01-01,False,False
    1999-01-02,False,False
    1999-01-03,False,False
    1999-01-04,False,False
    1999-01-06,True,False
    ...
    ```

- Parse a CSV dataset and put result into the file:

    ```sh
    $ ./production_calendar_parser.py -i data-sample.csv -o data-out.csv
    ```

- Use as a library to extract an additional information:
    
    ```sh
    In [1]: from csv import reader
    In [2]: from production_calendar_parser import ProductionCalendar
    In [3]: with open('data-sample.csv', encoding='utf-8') as f: 
       ...:     csv = reader(f) 
       ...:     next(csv) 
       ...:     calendar = ProductionCalendar.parse(csv) 
    In [4]: for year in calendar: 
       ...:     print(year.year, year.workdays, year.holidays)
    
    1999-01-01 251 114
    2000-01-01 250 116
    2001-01-01 251 114
    2002-01-01 250 115
    2003-01-01 250 115
    2004-01-01 251 115
    2005-01-01 248 117
    2006-01-01 248 117
    ...
    ```