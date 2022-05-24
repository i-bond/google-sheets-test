import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint as pp
import xmltodict
from datetime import date, datetime
from sqlalchemy import create_engine
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from dotenv import load_dotenv
from tzlocal import get_localzone
import os
import numpy as np

#postgres config
load_dotenv('vars.env')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
PG_TABLE = os.getenv('PG_TABLE')


def get_usd_rates():
    '''Возвращает актуальный курс USD/РУБ'''

    curr_date = date.today().strftime("%d/%m/%Y")
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={curr_date}'
    response = requests.get(url)
    valute_pairs = xmltodict.parse(response.content).get('ValCurs').get('Valute')
    usd_data = next(d for d in valute_pairs if d["CharCode"] == "USD")
    usd_rates = float(usd_data['Value'].replace(',', '.'))
    return usd_rates


def get_google_sheet_data(usd_rates=60.00,
                          gs_url='https://docs.google.com/spreadsheets/d/1G0Xfz-E4NBUvrTFaR5cVVHAYhY9OhZIH8S0QKgc4rLc'):
    '''Возвращает данные google sheets в виде Pandas DF, обрабатывает пустые ячейки заполняя их 0'''

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    cred = ServiceAccountCredentials.from_json_keyfile_name('creds/google_credentials.json', scope)
    gc = gspread.authorize(cred)
    google_sheet = gc.open_by_url(gs_url).get_worksheet(0)
    records = google_sheet.get_values()
    # pp.pprint(records)
    df = pd.DataFrame(records[1:], columns=records[0])
    df = df.replace(to_replace='', value=0)
    df = df.astype({'№': 'int64', 'заказ №': 'int64', 'стоимость,$': 'int64'})
    df['срок поставки'] = pd.to_datetime(df['срок поставки'], infer_datetime_format=True)
    df['стоимость в руб.'] = (df['стоимость,$'] * usd_rates).round(2)
    return df


def update_table(pg_user=PG_USER, pg_password=PG_PASSWORD, pg_host=PG_HOST,
                 pg_port=PG_PORT, pg_database=PG_DATABASE, pg_table=PG_TABLE):
    '''Обновляет данные в таблице'''

    usd_rates = get_usd_rates()
    print(usd_rates)
    df = get_google_sheet_data(usd_rates)
    print(df.head(10))

    DATABASE_URI = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'
    engine = create_engine(DATABASE_URI)
    try:
        with engine.connect() as conn:
            df.head(n=0).to_sql(name=pg_table, con=conn, index=False, if_exists='replace')  # create empty table
            df.to_sql(name=pg_table, con=conn, index=False, if_exists='append')
            print('Success - table updated!\n')
    except Exception as e:
        print("Failed to update table - ", e)


if __name__ == "__main__":
    tz = get_localzone()
    scheduler = BlockingScheduler()

    # Обновляет данные каждую минуту
    scheduler.add_job(update_table, 'cron', minute='*',
                      timezone=tz, misfire_grace_time=10)
    # Testing
    # scheduler.add_job(update_table, "interval", seconds=60, misfire_grace_time=5)

    scheduler.start()















