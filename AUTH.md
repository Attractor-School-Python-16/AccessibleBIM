# Установка авторизации Google

Источники:<br>
[Set up Google Sign-In for Faster Django Login Experience feat. Tech with Tim](https://www.youtube.com/watch?v=yO6PP0vEOMc)<br>
[Django Google OAuth](https://pylessons.com/django-google-oauth)

## Создание реквизитов

Для начала нужно зайти на сайт [Google Cloud](https://console.cloud.google.com/).
Создать проект, ввести название и организацию (можно не заполнять).

![image](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/01e7a8c6-5739-4390-9840-f8a7a2a6c867)

Затем зайти в вкладку “OAuth consent screen”.
Выбрать опцию “External” и нажать “Create”

![Akamai DevRel - Set up Google Sign-In for Faster Django Login Experience feat  Tech with Tim  yO6PP0vEOMc - 1536x864 - 4m36s](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/305205f3-df25-40bd-b4ff-5123263782cd)

Затем ввести название приложения и почту.
Лого, домен и прочее можно пока-что не заполнять.

![image](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/46c7b069-9e9b-4074-801a-421639c1eefd)
![image](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/435e226d-26d7-4593-be3f-4bcf44e2750b)

Затем на странице Scopes нажимаем “ADD OR REMOVE SCOPES” и выбираем те данные которые нам нужны, можно пока что email и профиль.

![image](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/dfca14aa-d228-4f50-bf46-7142ae7478e9)

Затем нажимаем “UPDATE” и “SAVE AND CONTINUE”.
Остальное можно пропустить и сохранить.


Теперь заходим во вкладку “Credentials” и нажимаем “CREATE CREDENTIALS” и выбираем “OAuth client ID”.

![image](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/9887ff92-8dad-44b0-9955-244bc4a51749)

Заполнить имя, и добавить url:<br>
http://127.0.0.1:8000/ <br>
http://127.0.0.1:8000/accounts/google/login/callback/ <br>
http://localhost:8000/accounts/google/login/callback/

Или другие домены которые вы используете

![image](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/7d2971a1-7697-47ce-aafe-a9f5f52d8e7e)

И после нажать “SAVE”.
Должно появиться окно “OAuth client created”. Можем скачать JSON.

## Подключение клиента

Теперь нужно зайти в само приложение и войти как Админ.
Зайти в админку Django. Во вкладке “SOCIAL ACCOUNTS” добавить Social application. Выбрать провайдер Google и ввести данные из ранее скачанного JSON файла.

![image](https://github.com/Attractor-School-Python-16/AccessibleBIM/assets/122436191/28ea261d-ec7f-4f73-90b5-d76f36093fb4)

Теперь в приложении работает авторизация через Google.
