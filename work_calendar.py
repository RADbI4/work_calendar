"""
Программа для вывода рабочих и выходных дней для людей, работающих 2/2
"""
import calendar
from calendar import Calendar, monthcalendar
import datetime
from Algorithms.func_programming.my_own_useful_funcs import implosive_attractor, list_engine, filter_engine, zip_engine
from functools import partial
import itertools

week_days_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

month_names = list(calendar.month_name)[1:]
now_date = implosive_attractor(partial(map, int), list)(datetime.date.today().strftime("%d-%m-%Y").split("-"))
work_days_in_all_year = {}

def work_days_in_year(first_day_of_work, month_of_work, year_of_work):
    # if year_of_work == now_date[2] + 1:
    #     return
    if year_of_work == 2024:
        return
    current_date = [first_day_of_work, month_of_work, year_of_work]
    data = list(itertools.chain.from_iterable(monthcalendar(current_date[2], current_date[1])))

    work_days = ([
        0 if x not in sorted(data[data.index(first_day_of_work):][::4] + data[data.index(first_day_of_work + 1):][::4])[
                      1:] else x for x in data])

    work_days_in_month = {
        month_names[month_of_work - 1]: implosive_attractor(lambda A, n=7: [A[i:i + n] for i in range(0, len(A), n)])(
            work_days)}
    last_work_day_of_current_month = datetime.datetime.strptime(
        f'{max(work_days_in_month[month_names[month_of_work - 1]][-1])}-{current_date[1]}-{current_date[2]}', "%d-%m-%Y")
    now_month_table = list_engine(partial(zip_engine, week_days_names), list(work_days_in_month.values())[0])
    work_days_in_month.update({
        list(work_days_in_month.keys())[0]: now_month_table
    })
    work_days_in_all_year.update(work_days_in_month)
    first_day_of_work = implosive_attractor(partial(map, int), list) \
            (
            (last_work_day_of_current_month + datetime.timedelta(days=3)).strftime("%d-%m-%Y").split("-")
        )
    work_days_in_year(first_day_of_work[0], first_day_of_work[1], first_day_of_work[2])




if __name__ == "__main__":
    # work_days_in_year(first_day_of_work=now_date[0], month_of_work=now_date[1], year_of_work=now_date[2])
    work_days_in_year(first_day_of_work=1, month_of_work=1, year_of_work=2023)
    pass
