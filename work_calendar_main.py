"""
Логика приложения.
"""
import work_calendar.src.work_calendar_constants as workc_const
from work_calendar_obj import Work_days_calculator, Table_plotter
from my_own_funcs import implosive_attractor


def workc_main(date):
    """
    Главная логика приложения
    :return:
    """
    # Определим данные для следующего класса и таблицу истинности рабочих/выходных дней.
    one_month_calculations = Work_days_calculator()
    one_month_calculations.work_days_in_month(date[0], date[1], date[2])
    Table_plotter().built_table(*one_month_calculations.color_set_mapper, **one_month_calculations.work_days_return)


# Для тестирования и локальных запусков
if __name__ == "__main__":
    now_date = (1, 1, 2023)
    workc_main(now_date)
    pass
