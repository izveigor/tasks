# Tasks ![account-tests](https://github.com/izveigor/tasks/actions/workflows/account-tests.yml/badge.svg) ![notifications-tests](https://github.com/izveigor/tasks/actions/workflows/notifications-tests.yml/badge.svg) ![tasks-tests](https://github.com/izveigor/tasks/actions/workflows/tasks-tests.yml/badge.svg) ![frontend-tests](https://github.com/izveigor/tasks/actions/workflows/frontend-tests.yml/badge.svg)
# Описание
Приложение для распределения заданий между членами команды.
![Главная страница](https://user-images.githubusercontent.com/68601180/210048890-d14aff51-9e6a-4b2f-b011-e0f03f90110a.png)
# Возможности
- Регистрация пользователей
- Вход пользователей
- Создать команду (стать администратором)
- Назначить задание
- Выполнить задание (удачно, неудачно)
- Назначить другого человека ответственным за сотрудника (возможность давать задания)
# Запуск (с помощью docker-compose)
Измените значения полей "EMAIL_HOST_USER" и "EMAIL_HOST_PASSWORD" в config файл (backend/account/config/.env.prod) на соответствующие значения
```
EMAIL_HOST_USER=username
EMAIL_HOST_PASSWORD=password
NOTIFICATIONS_HOST=tasks_notifications_production_server:50053
TASKS_HOST=tasks_tasks_production_server:50052
USERS_HOST=tasks_account_production_server:50051
```
```
./entrypoint.sh
```