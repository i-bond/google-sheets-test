# google-sheets-test
### Пререквизиты:   
Telegram API токен  
Telegram ID  


### Инструкции для запуска  
1. Создать файл google_credentials.json в папке creds/, добавить учетные данные service accounta  
2. Создать файл vars.env, добавить переменные, подставить Telegram API и Telegram ID  

API_TOKEN=123
MAIN_ID=123
PG_USER=postgres
PG_PASSWORD=postgres
PG_HOST=pgdatabase
PG_PORT=5432
PG_DATABASE=postgres
PG_TABLE=gs_table

3. Собрать образ и запустить контейнеры:
docker-compose build
docker-compose up

4. Можно подключиться к БД через pgAdmin:
localhost:7000
postgres:postgres





Полезные команды:
docker exec -u root -it google_sheets_test_gs_sync_data_1 bash
docker-compose down --volumes --rmi all
docker-compose logs gs_sync_data






















