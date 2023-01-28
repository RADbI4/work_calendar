"""
Логика приложения.
"""
from work_calendar_obj import Work_days_calculator, Table_plotter, telegram_floader
import json


def workc_main(date):
    """
    Главная логика приложения
    :return:
    """

    content = json.loads(date)
    date = content.get('date')
    # Определим данные для следующего класса и таблицу истинности рабочих/выходных дней.
    one_month_calculations = Work_days_calculator()
    one_month_calculations.work_days_in_month(date[0], date[1], date[2])
    # Создадим картинку на основе данных
    Table_plotter().built_table(*one_month_calculations.color_set_mapper, **one_month_calculations.work_days_return)
    # Отправим картинку в телеграм
    telegram_floader(content.get('chat_id'))


# Для тестирования и локальных запусков
if __name__ == "__main__":
    now_date = {"date": [1, 1, 2023]}
    now_date = json.dumps(now_date)
    workc_main(now_date)
    pass
