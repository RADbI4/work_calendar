import calendar
from my_own_funcs import implosive_attractor
from functools import partial
import datetime

now_date = implosive_attractor(partial(map, int), list)(datetime.date.today().strftime("%d-%m-%Y").split("-"))
week_days_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
month_names = list(calendar.month_name)[1:]