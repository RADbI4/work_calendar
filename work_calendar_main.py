"""
Логика приложения.
"""
import work_calendar.src.work_calendar_constants as workc_const
import src.work_calendar_funcs as workc_fucns


def workc_main():
    """
    Главная логика приложения
    :return:
    """
    # Определим все рабочие дни в году
    all_work_days_in_current_year = workc_fucns.work_days_in_year(first_day_of_work=workc_const.now_date[0],
                                                                  month_of_work=workc_const.now_date[1],
                                                                  year_of_work=workc_const.now_date[2])
    print(all_work_days_in_current_year)


# Для тестирования и локальных запусков
if __name__ == "__main__":
    workc_main()
