Создайте  многоконтейнерное приложение с помощью Docker Compose, которое состоит из веб-сервера Nginx, базы данных Redis и базы данных MySQL с volume для хранения файлов БД.



Написать docker-compose.yml файл для запуска нескольких сервисов: Nginx, Redis и MySQL.

Настроить volume  mysql_data для хранения данных базы данных MySQL.

services: Определение сервисов.

web:

image: Используемый образ, в данном случае nginx:latest, это официальный образ Nginx.

ports: Проброс порта 8080 на порт 80 контейнера.

redis:

image: redis:latest, это официальный образ Redis.

mysql:

image: Используемый образ mysql:8.0

environment: Переменные окружения для настройки базы данных MySQL.

volumes: mysql_data для хранения данных базы данных MySQL.

networks: Определение сети.

mynetwork: Сеть, которая соединяет все контейнеры.


*************

Команды для запуска:
docker compose up -d

http://localhost:8080

mysql_data — именованный Docker Volume. Благодаря ему данные MySQL сохранятся даже после удаления контейнера командой:
docker compose down

Но если выполнить:
docker compose down -v

то volume mysql_data тоже будет удалён вместе с данными.
