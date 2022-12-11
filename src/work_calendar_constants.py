import calendar
from my_own_funcs import implosive_attractor
from functools import partial
import datetime

now_date = implosive_attractor(partial(map, int), list)(datetime.date.today().strftime("%d-%m-%Y").split("-"))

week_days_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

month_names = list(calendar.month_name)[1:]

html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Таблица рабочих дней в году 2/2</title>
</head>
<body>"""

html_tail = """</body>
</html>"""

html_table_border = """<table border="1">"""

html_days = """<tr>
    <th>Mon</th>
    <th>tue</th>
    <th>wed</th>
    <th>thu</th>
    <th>fri</th>
    <th>sat</th>
    <th>sun</th>
   </tr>"""

html_table_end = """</table>"""

html_doc_end = """</body>
</html>"""
