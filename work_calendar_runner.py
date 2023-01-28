"""
Точка входа в приложение
"""
from work_calendar_main import workc_main
import traceback
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='work_d_in')


def callback(ch, method, properties, body):
    try:
        print("Started")
        workc_main(body)
        print("Finished")
        time.sleep(60)
    except Exception:
        print(traceback.format_exc())


channel.basic_consume(on_message_callback=callback, queue='work_d_in', auto_ack=True)
print(' [*] Waiting for messages, press CTRL+C to exit')
channel.start_consuming()
