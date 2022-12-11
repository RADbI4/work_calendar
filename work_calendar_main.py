"""
Логика приложения.
"""
import work_calendar.src.work_calendar_constants as workc_const
import src.work_calendar_funcs as workc_fucns
from my_own_funcs import implosive_attractor

def workc_main():
    """
    Главная логика приложения
    :return:
    """
    # Сначала определим все рабочие дни в году, затем создадим текст таблички html, затем сохраним файл html
    implosive_attractor(workc_fucns.work_days_in_year, workc_fucns.html_builder, workc_fucns.html_file_saver)(
        workc_const.now_date[0],
        workc_const.now_date[1],
        workc_const.now_date[2]
    )


# Для тестирования и локальных запусков
if __name__ == "__main__":
    # now_date = [1, 1, 2023]
    workc_main()
