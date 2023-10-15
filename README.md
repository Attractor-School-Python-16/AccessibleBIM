# accessibleBIM

# Видеокурсы для архитекторов

Описание проекта: ?

## Оглавление

- [Технологический стек](#технологический-стек)
- [Установка и запуск](#установка-и-запуск)
- [Использование](#использование)
- [Лицензия](#лицензия)

## Технологический стек

- **Язык программирования:** Python
- **Web-фреймворк:** Django
- **Контейнеризация:** Docker

## Установка и запуск

1. **Клонирование репозитория:**

```bash
git clone https://github.com/Em1rloneum/accessibleBIM.git
```

2. **Перед запуском убедитесь, что у вас установлен Docker.**  Если нет, то для начала работы установите Docker engine (движок докера)
по инструкции отсюда: https://docs.docker.com/install/linux/docker-ce/ubuntu/ для Ubuntu и Linux Mint или
отсюда https://docs.docker.com/docker-for-mac/install/ для Mac.

3. Добавить файл .env в корневую директорию
4. В терминале проекта после запустить команду docker-compose build, после запустить команду docker-compose up и все должно работать.

**При добавлении новых файлов фикстур:** 
1) добавлять в название номер следующий за последним (сейчас последний файл 09_socialaccount.json, значит следующий должен начинаться с 10_...json)

2) далее, название новых фикстур нужно добавить в файл docker-compose.yml - в сервисе backend:, в строке: command: >
```bash
sh -c "python manage.py migrate &&
for fixture in 01_auth.json 02_accounts.json 03_currencies.json 04_modules.json 05_quiz_bim.json 06_step.json 07_tasks.json 08_sites.json 09_client_secret_532801370309_el6kjnghd31rvgrps9c8i91o4gr0n1kl_apps.json 10_socialaccount.json вот здесь; do ``` - важно все в одной строке писать, иначе выдает ошибку

Если появляется необходимость **создать миграцию**, (до команды docker-compose up) нужно запустить в терминале следующие команды:
```bash
docker-compose build
docker-compose run backend python manage.py makemigrations
docker-compose run backend python manage.py migrate
docker-compose up```

Но можно и без перезапуска (docker-compose build)
```bash
docker-compose exec backend ./manage.py makemigrations
docker-compose exec backend ./manage.py migrate```

