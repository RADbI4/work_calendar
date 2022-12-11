"""
Логика приложения.
"""
import work_calendar.src.work_calendar_constants as wc_const
import src.work_calendar_funcs as wc_fucns


def wc_main():
    """
    Главная логика приложения
    :return:
    """
    # Определим все рабочие дни в году
    all_work_days_in_current_year = wc_fucns.work_days_in_year(first_day_of_work=wc_const.now_date[0],
                                                               month_of_work=wc_const.now_date[1],
                                                               year_of_work=wc_const.now_date[2])
    print(all_work_days_in_current_year)

# Для тестирования и локальных запусков
if __name__ == "__main__":
    wc_main()