# Установка авторизации Google

Источники:<br>
[Set up Google Sign-In for Faster Django Login Experience feat. Tech with Tim](https://www.youtube.com/watch?v=yO6PP0vEOMc)<br>
[Django Google OAuth](https://pylessons.com/django-google-oauth)

## Создание реквизитов

Для начала нужно зайти на сайт [Google Cloud](https://console.cloud.google.com/).
Создать проект, ввести название и организацию (можно не заполнять).

Затем зайти в вкладку “OAuth consent screen”.
Выбрать опцию “External” и нажать “Create”

Затем ввести название приложения и почту.
Лого, домен и прочее можно пока-что не заполнять.

Затем на странице Scopes нажимаем “ADD OR REMOVE SCOPES” и выбираем те данные которые нам нужны, можно пока что email и профиль.

Затем нажимаем “UPDATE” и “SAVE AND CONTINUE”.
Остальное можно пропустить и сохранить.
Теперь заходим во вкладку “Credentials” и нажимаем “CREATE CREDENTIALS” и выбираем “OAuth client ID”.

Заполнить имя, и добавить url:<br>
http://127.0.0.1:8000/ <br>
http://localhost:8000/google/login/callback/

И после нажать “SAVE”.
Должно появиться окно “OAuth client created”. Можем скачать JSON.

## Подключение клиента

Теперь нужно зайти в само приложение и войти как Админ.
Зайти в админку Django. Во вкладке “SOCIAL ACCOUNTS” добавить Social application. Выбрать провайдер Google и ввести данные из ранее скачанного JSON файла.