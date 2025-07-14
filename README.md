Скачать все это в папку. В e.env записать адрес БД

Затем

cd <ВАША_ПАПКА>

sudo docker-compose up

Указывать ничего не надо, автоматом чтение docker-compose.yaml и сборка.

Теперь у вас API для базы данных!

-------------

Изменения:

-AIOGRAM изменена сборка запросов. Теперь красивее

-FAST API добавлены routes "Получать по условию" "Удалять по условию"

-FAST API добавлено асихронное исполнение Session

-Добавлен logger в try-except

- docker-compose теперь из трех контейнеров - aiogram_app | fastapi_app | postgres