from datetime import date
from dateutil.relativedelta import relativedelta


def get_first_day_of_week(datetime):
    _year = datetime.year
    _month = datetime.month
    _day = datetime.day
    day_of_week = date(_year, _month, _day).isoweekday()

    if day_of_week == 7:
        day_of_week = 0

    return datetime - relativedelta(days=day_of_week)


def get_last_day_of_week(datetime):
    _year = datetime.year
    _month = datetime.month
    _day = datetime.day
    day_of_week = date(_year, _month, _day).isoweekday()

    if day_of_week == 7:
        day_of_week = 0
    
    return datetime + relativedelta(days=6 - day_of_week)

if __name__ == '__main__':
    # _datetime = '2024-11-12 17:36:57.948618'
    # print(get_first_day_of_week(str(timezone.now)))
    # print(get_last_day_of_week(_datetime))
    print('Semana começa:' ,get_first_day_of_week(date.today()))
    print('Semana termina:', get_last_day_of_week(date.today()))