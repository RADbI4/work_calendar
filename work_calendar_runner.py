"""
Точка входа в приложение
"""
from work_calendar_main import workc_main
import traceback
import time

try:
    while True:
        print("Started")
        workc_main()
        print("Finished")
        time.sleep(60)
except Exception:
    print(traceback.format_exc())