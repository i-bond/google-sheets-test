# google-sheets-test
Скрипт для синхронизации данных между Google Sheets и Postgres DB  
Telegram бот для уведомления о сроках поставки  

**DashBoard Link**: https://datastudio.google.com/reporting/8fb1a12b-18ca-46ea-9dc2-b0740f786788  
**Google Sheets**: https://docs.google.com/spreadsheets/d/1G0Xfz-E4NBUvrTFaR5cVVHAYhY9OhZIH8S0QKgc4rLc  


### Пререквизиты:   
Telegram API токен  
Telegram ID  


### Инструкции для запуска  
1. Создать файл google_credentials.json в папке creds/, добавить учетные данные GCP service accounta  
2. Создать файл vars.env, добавить переменные, подставить Telegram API и Telegram ID  
```
API_TOKEN=123
MAIN_ID=123
PG_USER=postgres
PG_PASSWORD=postgres
PG_HOST=pgdatabase
PG_PORT=5432
PG_DATABASE=postgres
PG_TABLE=gs_table
```
3. Собрать образ и запустить контейнеры:
```
docker-compose build
docker-compose up
```
4. Подключиться к БД можно через pgAdmin:
```
localhost:7000
postgres:postgres
```

Полезные команды:
```
docker exec -u root -it google_sheets_test_gs_sync_data_1 bash
docker-compose down --volumes --rmi all
docker-compose logs gs_sync_data
```





















