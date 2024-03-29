"""
Программа для вывода рабочих и выходных дней для людей, работающих 2/2
"""
import datetime
import itertools
from calendar import monthcalendar
from functools import partial
from work_calendar_constants import week_days_names
import work_calendar_constants as const
from my_own_funcs import implosive_attractor, list_engine
from matplotlib import pyplot as plt
import pika
import json
from base64 import b64encode


class Work_days_calculator:
    """
    Класс- для работы с выходными днями.
    """

    def __init__(self):
        self.work_days_return = {}
        self.color_set_mapper = None
        pass

    def work_days_in_month(self, first_day_of_work, month_of_work, year_of_work):
        """
        Метод возвращает таблицу из месяца и рабочих дней.
        :return:
        {
        {'November': [
        {'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0, 'sat': 0, 'sun': 0},
        {'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0, 'sat': 0, 'sun': 11},
        {'mon': 12, 'tue': 0, 'wed': 0, 'thu': 15, 'fri': 16, 'sat': 0, 'sun': 0},
        {'mon': 19, 'tue': 20, 'wed': 0, 'thu': 0, 'fri': 23, 'sat': 24, 'sun': 0},
        {'mon': 0, 'tue': 27, 'wed': 28, 'thu': 0, 'fri': 0, 'sat': 31, 'sun': 0}
        ]
        }
        """

        current_date = [first_day_of_work, month_of_work, year_of_work]
        month_days = monthcalendar(current_date[2], current_date[1])
        data = list(itertools.chain.from_iterable(month_days))

        # Получим только рабочие дни
        work_days = ([
            0 if x not in sorted([first_day_of_work] + data[data.index(first_day_of_work):][::4] + data[data.index(
                first_day_of_work + 1):][::4])[
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

        self.color_set_mapper = [
            [list_engine(lambda to_boolean: 'green' if to_boolean == 0 else 'red', week) for week in month] for month in
            work_days_in_month.values()]

        work_days_in_month.update({
            list(work_days_in_month.keys())[0]: month_days
        })
        self.work_days_return.update(work_days_in_month)

        # Возвращаем первый рабочий день месяца
        return implosive_attractor(partial(map, int), list) \
                (
                (last_work_day_of_current_month + datetime.timedelta(days=3)).strftime("%d-%m-%Y").split("-")
            )

    def work_days_in_year(self, first_day_of_work, month_of_work, year_of_work):
        """
        Метод возвращает таблицу из месяцев и рабочих дней.
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

        # Вычислим дату первого рабочего дня в следующем месяце
        first_day_of_work = self.work_days_in_month(first_day_of_work, month_of_work, year_of_work)

        # Рекурсионно вычислим следующий месяц
        self.work_days_in_year(first_day_of_work[0], first_day_of_work[1], first_day_of_work[2])
        return self.work_days_return


class Table_plotter:
    """
    Класс, отвечающий за построение таблицы в MatPlotLib.
    """

    def __init__(self):
        pass

    @staticmethod
    def built_table(*color_map, **data):
        """
        Строит таблицу на основе полученных данных.
        :return:
        """
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # cell_text = [list(x.values()) for x in data.get(*data.keys())]

        cell_text = data.get(*data.keys())

        fig, ax = plt.subplots()
        ax.set_title(f"{list(data.keys())[0]}")
        the_table = ax.table(cellText=cell_text,
                             cellColours=color_map[0],
                             colLabels=week_days_names,
                             loc='center')
        ax.axis('off')
        data = {'fname': f'work_days_of_month.png'}
        plt.savefig(data.get('fname'))
        plt.close()
        return data


def pub_t_tg_floader(data: dict):
    """
    Публикует сообщение в очередь RabbitMQ work_d_out
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='work_d_out')
    with open('work_days_of_month.png', 'rb') as file_to_floader:
        # file_to_floader = file_to_floader.read()
        # file_to_floader = file_to_floader.decode('utf-8')
        file_to_floader = b64encode(file_to_floader.read()).decode('utf-8')
        data['fdata'] = file_to_floader
        data = json.dumps(data)
        channel.basic_publish(exchange='', routing_key='work_d_out', body=data)


if __name__ == "__main__":
    # a = Work_days_calculator().work_days_in_year(1, 1, 2023)
    # b = Work_days_calculator()
    # a = b.work_days_in_month(26, 1, 2023)
    # Table_plotter().built_table(*b.color_set_mapper, **b.work_days_return)
    pass
