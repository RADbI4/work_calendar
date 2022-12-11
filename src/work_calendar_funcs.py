"""
Программа для вывода рабочих и выходных дней для людей, работающих 2/2
"""
import datetime
import itertools
from calendar import monthcalendar
from functools import partial

from work_calendar_constants import month_names, week_days_names, now_date
from my_own_funcs import implosive_attractor, list_engine, zip_engine


def work_days_in_year(first_day_of_work, month_of_work, year_of_work):
    """
    Функция возвращает таблицу из месяцев и рабочих дней.
    :param first_day_of_work: число- первый рабочий день.
    :param month_of_work: число- месяц первого рабочего дня
    :param year_of_work: год работы
    :return: словарь вида:
    {
    {'November': [
    {'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0, 'sat': 0, 'sun': 0},
    {'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0, 'sat': 0, 'sun': 11},
    {'mon': 12, 'tue': 0, 'wed': 0, 'thu': 15, 'fri': 16, 'sat': 0, 'sun': 0},
    {'mon': 19, 'tue': 20, 'wed': 0, 'thu': 0, 'fri': 23, 'sat': 24, 'sun': 0},
    {'mon': 0, 'tue': 27, 'wed': 28, 'thu': 0, 'fri': 0, 'sat': 31, 'sun': 0}
    ],

    'December': [
    {'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0, 'sat': 0, 'sun': 0},
    {'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0, 'sat': 0, 'sun': 11},
    {'mon': 12, 'tue': 0, 'wed': 0, 'thu': 15, 'fri': 16, 'sat': 0, 'sun': 0},
    {'mon': 19, 'tue': 20, 'wed': 0, 'thu': 0, 'fri': 23, 'sat': 24, 'sun': 0},
    {'mon': 0, 'tue': 27, 'wed': 28, 'thu': 0, 'fri': 0, 'sat': 31, 'sun': 0}
    ]
    },
    ....
    Ключи- названия месяцев.
    Значения- список недель с днями. 0 -не рабочий день либо день другого месяца.
    Числа- рабочие дни.
    """
    # Инициализируем доп. память для словаря
    work_days_in_all_year = {}

    # Конечное условие функции- следующий год
    if year_of_work == now_date[2] + 1:
        return
    current_date = [first_day_of_work, month_of_work, year_of_work]
    data = list(itertools.chain.from_iterable(monthcalendar(current_date[2], current_date[1])))

    # Получим только рабочие дни
    work_days = ([
        0 if x not in sorted(data[data.index(first_day_of_work):][::4] + data[data.index(first_day_of_work + 1):][::4])[
                      1:] else x for x in data])

    # Получим рабочие дни в месяце
    work_days_in_month = {
        month_names[month_of_work - 1]: implosive_attractor(lambda A, n=7: [A[i:i + n] for i in range(0, len(A), n)])(
            work_days)}
    # Определим последний и рабочий день в месяце
    last_work_day_of_current_month = datetime.datetime.strptime(
        f'{max(work_days_in_month[month_names[month_of_work - 1]][-1])}-{current_date[1]}-{current_date[2]}',
        "%d-%m-%Y")

    # Создаём таблицу рабочих дней.
    now_month_table = list_engine(partial(zip_engine, week_days_names), list(work_days_in_month.values())[0])

    work_days_in_month.update({
        list(work_days_in_month.keys())[0]: now_month_table
    })
    work_days_in_all_year.update(work_days_in_month)
    first_day_of_work = implosive_attractor(partial(map, int), list) \
            (
            (last_work_day_of_current_month + datetime.timedelta(days=3)).strftime("%d-%m-%Y").split("-")
        )
    # Рекурсионно вычислим следующий месяц
    work_days_in_year(first_day_of_work[0], first_day_of_work[1], first_day_of_work[2])
    return work_days_in_all_year


# Для тестирования и локальных запусков
if __name__ == "__main__":
    wc_days = work_days_in_year(first_day_of_work=now_date[0], month_of_work=now_date[1], year_of_work=now_date[2])
    pass
