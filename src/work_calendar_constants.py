
from my_own_funcs import implosive_attractor
from functools import partial
import datetime

now_date = implosive_attractor(partial(map, int), list)(datetime.date.today().strftime("%d-%m-%Y").split("-"))

week_days_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

