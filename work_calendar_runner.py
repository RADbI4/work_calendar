"""
Точка входа в приложение
"""
from work_calendar_main import wc_main
import traceback

try:
    while True:
        wc_main()
except Exception:
    print(traceback.format_exc())