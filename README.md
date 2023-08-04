# posts_app

`posts_app` - Приложение, позволяющее регистрироваться и создавать посты. В приложении реализованы веб-интерфейс и REST API.

## Системные требования
- Python 3.11+
- Works on Linux, Windows, macOS

## Основные технологии:
- Python 3.11
- Django
- Django Rest Framework
- SQLite
- Gunicorn


## Как запустить проект:

Для запуска в проект вложена конфигурация docker-compose. После запуска docker-compose сайт будет доступен по адресу: `http://<host address>/`.

API будет доступно по адресу `http://<host address>/api/`.

Необходимо выполнить следующие шаги:
- Склонируйте репозиторий с GitHub и перейдите в папку проекта, где расположен файл docker-compose.yml:
```
git clone git@github.com:KostKH/posts_app.git
cd posts_app/infra_posts_app
```
- Проверьте, что на машине / сервере установлены `docker` и `docker compose`

- Cоздайте в папке `infra_posts_app` файл `.env`  для хранения переменных окружения. Можно создать его из вложенного образца `env_example.env`:
```
cp env_example.env .env
```
- Откройте файл .env в редакторе и поменяйте секретный ключ.
- Установите и запустите приложение в контейнере. (Возможно, вам придется добавить `sudo` перед текстом команды):
```
docker compose up -d
```
- Запустите миграции, соберите статику:
```
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic
```
После этого приложение будет готово к работе.

## Тесты
Для запуска тестов, после того, как вы запустили приложение в докере (см.предыдущие шаги), находясь в папке `infra_posts_app`, выполните следующие команды:
```
docker-compose exec app bash
python manage.py test
exit
```

## Основные URL у сайта:
```
http:/<host_address>/ - Главная страница, выводит список пользователей
http:/<host_address>/auth/signup/ - Регистрация нового пользователя
http:/<host_address>/auth/login/ - Вход на сайт
http:/<host_address>/users/<id>/posts/ - Просмотр постов пользователя с номером <id>
http:/<host_address>/posts/new/ - Создание нового поста
```

## Основные эндпойнты у API:
```
http:/<host_address>/api/users/ - GET, просмотр списка пользователей
http:/<host_address>/api/auth/signin/ - POST, регистрация нового пользователя
http:/<host_address>/api/auth/login/ - POST, запрос на получение токена авторизации
http:/<host_address>/api/users/<id>/posts/ - GET, Просмотр постов пользователя <id>
http:/<host_address>/api/posts/ - POST: Создание нового поста
http:/<host_address>/api/posts/<id>/ - DELETE: Удаление поста
```

## Документация по API:
После запуска сервиса документация по API будет доступна по ссылке:
- `<host_address>/docs/`

## О программе:

Автор: Константин Харьков