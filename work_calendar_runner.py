"""
Точка входа в приложение
"""
from work_calendar_main import workc_main
import traceback

try:
    while True:
        workc_main()
except Exception:
    print(traceback.format_exc())