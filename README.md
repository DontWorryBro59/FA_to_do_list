# FA_to_do_list

# Мой учебный(pet) проект на FastAPI

## Описание
Мой проект на FastAPI - это веб-приложение, которое позволяет пользователям выполнять различные задачи. Приложение разработано с использованием следующих библиотек:
- FastAPI: современный, быстрый и легкий в использовании фреймворк для создания веб-приложений на Python.
  (были реализованы различные эндпоинты для работы с БД на postgresql)
- SQLAlchemy: библиотека для работы с базами данных, которая предоставляет мощные инструменты для работы с SQL.
  (использовалась orm часть библиотеки)
- Pydantic: библиотека для проверки данных и создания моделей данных.
  (были использованы модели(schemas) для валидации входящей информации в API)
- Uvicorn: ASGI-сервер для запуска приложений на Python.

## Установка
Для установки проекта выполните следующие шаги:
1. Клонируйте репозиторий: `git clone https://github.com/"project_name"`
2. Перейдите в каталог проекта: `cd "projectname"`
3. Установите зависимости: `pip install -r requirements.txt`
4. Запустите приложение: `uvicorn main:app --reload`

## Использование
После запуска приложения вы можете получить доступ к нему по адресу `http://localhost:8000`. Приложение предоставляет следующие возможности:
- Создание, редактирование и удаление задач
- Создание, редактирование и удаление пользователей
- Назначение задач пользователям
- Изменение статуса задачи
- Просмотр списка задач

## Документация
Документация API доступна по адресу `http://localhost:8000/docs`. Она содержит подробное описание всех доступных эндпоинтов и параметров запросов.

## Тестирование
Для запуска тестов выполните команду `pytest`.

