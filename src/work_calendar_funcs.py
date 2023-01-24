"""
Программа для вывода рабочих и выходных дней для людей, работающих 2/2
"""
import datetime
import itertools
from calendar import monthcalendar
from functools import partial

import work_calendar_constants as const
from my_own_funcs import implosive_attractor, list_engine, zip_engine, str_engine

# Инициализируем доп. память для словаря
work_days_in_all_year = {}

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
    # Для тестов
    # if year_of_work == 2024:
    #     return

    # Конечное условие функции- следующий год
    if year_of_work == const.now_date[2] + 1:
        return
    current_date = [first_day_of_work, month_of_work, year_of_work]
    data = list(itertools.chain.from_iterable(monthcalendar(current_date[2], current_date[1])))

    # Получим только рабочие дни
    work_days = ([
        0 if x not in sorted([first_day_of_work] + data[data.index(first_day_of_work):][::4] + data[data.index(first_day_of_work + 1):][::4])[
                      1:] else x for x in data])

    # Получим рабочие дни в месяце
    work_days_in_month = {
        const.month_names[month_of_work - 1]: implosive_attractor(
            lambda A, n=7: [A[i:i + n] for i in range(0, len(A), n)])(
            work_days)}
    # Определим последний и рабочий день в месяце
    try:
        last_work_day_of_current_month = datetime.datetime.strptime(
            f'{max(work_days_in_month[const.month_names[month_of_work - 1]][-1])}-{current_date[1]}-{current_date[2]}',
            "%d-%m-%Y")
    except BaseException as e:
        # Если нет рабочих дней в последней неделе месяца, то они точно есть в предпоследней
        last_work_day_of_current_month = datetime.datetime.strptime(
            f'{max(work_days_in_month[const.month_names[month_of_work - 1]][-2])}-{current_date[1]}-{current_date[2]}',
            "%d-%m-%Y")
    # Создаём таблицу рабочих дней.
    now_month_table = list_engine(partial(zip_engine, const.week_days_names), list(work_days_in_month.values())[0])

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


def html_builder(table_for_build):
    """
    Создаёт строку для HTML файла таблицы рабочих дней.
    :param table_for_build:
    :return:
    """
    color_choiser = lambda int_for_coloring: 'bgcolor="#92ff15"' if int_for_coloring ==0 else 'bgcolor="#d53e07"'

    html_table_row_builder = lambda dict_to_html_row: \
        '<tr><td {}>{}' \
        '</td><td {}>{}' \
        '</td><td {}>{}' \
        '</td><td {}>{}' \
        '</td><td {}>{}' \
        '</td><td {}>{}' \
        '</td><td {}>{}</td></tr>\n'.format(
            color_choiser(dict_to_html_row['mon']),
            dict_to_html_row['mon'],
            color_choiser(dict_to_html_row['tue']),
            dict_to_html_row['tue'],
            color_choiser(dict_to_html_row['wed']),
            dict_to_html_row['wed'],
            color_choiser(dict_to_html_row['thu']),
            dict_to_html_row['thu'],
            color_choiser(dict_to_html_row['fri']),
            dict_to_html_row['fri'],
            color_choiser(dict_to_html_row['sat']),
            dict_to_html_row['sat'],
            color_choiser(dict_to_html_row['sun']),
            dict_to_html_row['sun'],
        )

    table_builder = lambda month_to_build_table: \
        const.html_table_border \
        + "<caption>{}</caption>\n   ".format(month_to_build_table) \
        + const.html_days \
        + "   ".join(
        list_engine(html_table_row_builder, table_for_build[month_to_build_table])) \
        + const.html_table_end

    html_text = const.html_header + str_engine(table_builder, list(table_for_build.keys())) + const.html_tail
    return html_text


def html_file_saver(text_for_html_file):
    with open("work_days_of_current_year.html", "w+") as html_file:
        html_file.write(text_for_html_file)


# Для тестирования и локальных запусков
if __name__ == "__main__":
    # html_file_saver(html_builder(work_days_in_year(first_day_of_work=const.now_date[0],
    #                                                month_of_work=const.now_date[1],
    #                                                year_of_work=const.now_date[2])))

    # html_file_saver(html_builder(work_days_in_year(first_day_of_work=1, month_of_work=1, year_of_work=2023)))
    pass
