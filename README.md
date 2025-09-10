Скачать папку. В e.env записать адрес БД

Затем

cd home/../Desktop/fastapi_app

sudo docker build . -t my_fastapi

sudo docker run -p 80:80 my_fastapi
p 443:443 если HTTPS


Теперь у вас API для базы данных!

-------------

Изменения:

- FAST API добавлены routes "Удалять по условию"

- FAST API добавлено асихронное исполнение Session

- Добавлен logger
