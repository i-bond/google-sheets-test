import os
from apscheduler.schedulers.blocking import BlockingScheduler
import telebot
from datetime import datetime
from tzlocal import get_localzone
from dotenv import load_dotenv
from sqlalchemy import create_engine

#bot config
load_dotenv('vars.env')
API_TOKEN = os.getenv('API_TOKEN')
MAIN_ID = os.getenv('MAIN_ID')
#postgres config
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
PG_TABLE = os.getenv('PG_TABLE')

bot = telebot.TeleBot(API_TOKEN)


def get_expiring_orders(pg_user, pg_password, pg_host, pg_port, pg_database):
    '''Возвращает 2 списка заказов, сроки поставки которых истекают сегодня и завтра'''

    DATABASE_URI = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'
    engine = create_engine(DATABASE_URI)
    expire_today, expire_tomorrow = [], []
    try:
        with engine.connect() as conn:
            expire_today = conn.execute(
                '''
                SELECT "заказ №", "стоимость,$", "срок поставки" FROM gs_table
                WHERE "срок поставки" = CURRENT_DATE
                '''
            )
            expire_tomorrow = conn.execute(
                '''
                SELECT "заказ №", "стоимость,$", "срок поставки" FROM gs_table
                WHERE "срок поставки" = CURRENT_DATE+1
                '''
            )
    except Exception as e:
        print("Failed to update table - ", e)

    return expire_today, expire_tomorrow



def send_notifications(main_id=MAIN_ID, pg_user=PG_USER, pg_password=PG_PASSWORD, pg_host=PG_HOST, pg_port=PG_PORT, pg_database=PG_DATABASE):
    '''Отправляет уведомления в телеграм по id'''

    expire_today, expire_tomorrow = get_expiring_orders(pg_user, pg_password, pg_host, pg_port, pg_database)


    for order in expire_today:
        order_n = order[0]
        order_val = order[1]
        exp_date = order[2].strftime("%d-%m-%Y")
        msg = f"Срок для выполения заказа №{order_n} стоимостью ${order_val} истекает сегодня ({exp_date})"
        bot.send_message(main_id, text=msg, parse_mode='HTML')

    for order in expire_tomorrow:
        order_n = order[0]
        order_val = order[1]
        exp_date = order[2].strftime("%d-%m-%Y")
        msg = f"Срок для выполения заказа №{order_n} стоимостью ${order_val} истекает завтра ({exp_date})"
        bot.send_message(main_id, text=msg, parse_mode='HTML')

    print('Notifications Sent!')


if __name__ == '__main__':
    tz = get_localzone()
    scheduler = BlockingScheduler()

    # Отправляет уведомления каждое утро в 9:05
    # scheduler.add_job(send_notifications, 'cron', hour=9, minute=5,
    #                timezone=tz, misfire_grace_time=10)
    # Testing
    scheduler.add_job(send_notifications, "interval", seconds=60, misfire_grace_time=5,
                      next_run_time=datetime.now())

    scheduler.start()





